import av
import sys
import time
import threading
import logging
import tkinter as tk
from PIL import ImageTk, Image
from typing import Tuple, Dict

logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used

#FIXME: sometimes there is a segmentation fault when seeking specific second

class TkinterVideo(tk.Label):

    def __init__(self, master, scaled: bool = True, *args, **kwargs):
        super(TkinterVideo, self).__init__(master, *args, **kwargs)

        self.path = ""
        self._load_thread = None

        self._paused = True
        self._stop = True

        self._container = None

        self._current_img = None
        self._current_frame_Tk = None
        self._frame_number = 0
        self._time_stamp = 0

        self._current_frame_size = (0, 0)

        self._seek = False
        self._seek_sec = 0

        self._video_meta = {
            "file": "",
            "duration": 0, # duration of the video
            "framerate": 0, # frame rate of the video
            "framesize": (0, 0) # tuple containing frame height and width of the video

        }   

        self.set_scaled(scaled)


        self.bind("<<Destroy>>", self.stop)
        self.bind("<<FrameGenerated>>", self._display_frame)
    
    def set_size(self, size: Tuple[int, int]):
        """ sets the size of the video """
        self.set_scaled(False)
        self._current_frame_size = size

    def _resize_event(self, event):

        self._current_frame_size = event.width, event.height

        if self._paused and self._current_img and self.scaled:
            proxy_img = self._current_img.copy().resize(self._current_frame_size)
            self._current_imgtk = ImageTk.PhotoImage(proxy_img)
            self.config(image=self._current_imgtk)


    def set_scaled(self, scaled: bool):
        self.scaled = scaled

        if scaled:
            self.bind("<Configure>", self._resize_event)

        else:
            self.unbind("<Configure>")

    def _set_frame_size(self, event=None):
        """ sets frame size to avoid unexpected resizing """

        self._video_meta["framesize"] = (self._container.streams.video[0].width, self._container.streams.video[0].height)

        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._video_meta["framesize"], (255, 0, 0, 0)))
        self.config(width=150, height=100, image=self.current_imgtk)

    def _load(self, path):
        """ load's file from a thread """

        current_thread = threading.current_thread()

        with av.open(path) as self._container:

            self._container.streams.video[0].thread_type = "AUTO"
            
            # print(self._container.duration)
            self._container.fast_seek = True
            self._container.discard_corrupt = True

            stream = self._container.streams.video[0]

            try:
                self._video_meta["framerate"] = int(stream.average_rate)

            except TypeError:
                raise TypeError("Not a video file")

            
            try:

                self._video_meta["duration"] = float(stream.duration * stream.time_base)
                self.event_generate("<<Duration>>")  # duration has been found

            except TypeError:  # the video duration cannot be found, this can happen for mkv files
                pass

            self._frame_number = 0

            self._set_frame_size()

            self.stream_base = stream.time_base

            while self._load_thread == current_thread and not self._stop:
                
                if self._seek: # seek to specific second
                    self._container.seek(self._seek_sec*1000000 , whence='time', backward=True, any_frame=False) # the seek time is given in av.time_base, the multiplication is to correct the frame
                    self._seek = False
                    self._frame_number = self._video_meta["framerate"] * self._seek_sec

                    self._seek_sec = 0

                if self._paused:
                    continue
                
                try:
                    frame = next(self._container.decode(video=0))

                    self._time_stamp = float(frame.pts * stream.time_base)

                    self._current_img = frame.to_image()

                    self._frame_number += 1
            
                    self.event_generate("<<FrameGenerated>>")

                    if self._frame_number % self._video_meta["framerate"] == 0:
                        self.event_generate("<<SecondChanged>>")

                except (StopIteration, av.error.EOFError):
                    break
                    
                except tk.TclError:
                    break

        self._frame_number = 0
        self._paused = True
        self._load_thread = None

        self._container = None
        
        try:
            self.event_generate("<<Ended>>")  # this is generated when the video ends

        except tk.TclError:
            pass

    def load(self, path: str):
        """ loads the file from the given path """
        self.path = path
        self._load_thread = threading.Thread(target=self._load, args=(path, ), daemon=True)
        self._load_thread.start()

    def stop(self):
        """ stops reading the file """
        self._paused = True
        self._stop = True

    def pause(self):
        """ pauses the video file """
        self._paused = True

    def play(self):
        """ plays the video file """
        self._paused = False
        self._stop = False

        if not self._load_thread:
            # print("loading new thread...")
            self._load_thread = threading.Thread(target=self._load,  args=(self.path, ), daemon=True)
            self._load_thread.start()

    def is_paused(self):
        """ returns if the video is paused """
        return self._paused

    def video_info(self) -> Dict:
        """ returns dict containing duration, frame_rate, file"""
        return self._video_meta

    def metadata(self) -> Dict:
        """ returns metadata if available """
        if self._container:
            return self._container.metadata

        return {}

    def current_frame_number(self) -> int:
        """ return current frame number """
        return self._frame_number

    def current_duration(self) -> float:
        """ returns current playing duration in sec """
        return self._time_stamp
    
    def _display_frame(self, event):
        """ displays the frame on the label """

        if self.scaled:
            self._current_img =  self._current_img.resize(self._current_frame_size)

        self.current_imgtk = ImageTk.PhotoImage(self._current_img)
        self.config(image=self.current_imgtk)

    def seek(self, sec: int):
        """ seeks to specific time""" 

        self._seek = True
        self._seek_sec = sec            
            

    