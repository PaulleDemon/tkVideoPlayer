import av
import sys
import time
import threading
import logging
import tkinter as tk
from PIL import ImageTk, Image
from typing import Tuple, Dict

logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used, make sure you


# did set range correctly


class TkinterVideo(tk.Label):

    def __init__(self, master, scaled: bool = True, *args, **kwargs):
        super(TkinterVideo, self).__init__(master, *args, **kwargs)

        self.path = ""
        self._load_thread = None

        self._pause = True
        self._stop = True

        self._container = None

        self._current_img = None
        self._current_frame_Tk = None
        self._frame_number = 0

        self._video_meta = {
            "file": "",
            "duration": 0,
            "framerate": 0,

        }

        self.bind("<<Destroy>>", self.stop)
        self.bind("<<FrameGenerated>>", self._display_frame)
    
    def set_scaled(self, scaled: bool):
        self.scaled = scaled

        if scaled:
            self.bind("<Configure>", self._resize_event)

        else:
            self.unbind("<Configure>", self._resize_event)

    def _load(self, path):
        """ load's file from a thread """

        current_thread = threading.current_thread()
        self._container = av.open(path)

        try:
            self._video_meta["frame_rate"] = int(self._container.streams.video[0].average_rate)

        except TypeError:
            raise TypeError("Not a video file")

        
        try:
            self._video_meta["duration"] = float(
                self._container.streams.video[0].duration * self._container.streams.video[0].time_base)

        except TypeError:  # the video duration cannot be found, this can happen for mkv files
            pass

            
        for frame_number, frame in enumerate(self._container.decode(video=0)):  # container.decode yields generator

            if self._load_thread != current_thread or self._stop:
                break

            self._current_img = frame.to_image() # if memory error try setting height and with expcitily, refer pyav docs, to_image()

            self._frame_number = frame_number
            self.event_generate("<<FrameGenerated>>")
        
        self._container.close()
        self._frame_number = 0
        self._playing = False
        self._paused = True
        self.event_generate("<<Ended>>")  # this is generated when the video ends

    def load(self, path: str):
        """ loads the file from the given path """

        self._load_thread = threading.Thread(target=self._load, args=(path, ), daemon=True)
        self._load_thread.start()

    def stop(self):
        """ stops reading the file """
        self._pause = True
        self._stop = True

    def pause(self):
        """ pauses the video file """
        self._pause = True

    def play(self):
        """ plays the video file """
        self._pause = False
        self._stop = False

    def video_info(self) -> Dict:
        """ returns dict containing duration, frame_rate, file"""
        return self._video_meta

    def current_frame_number(self) -> int:
        """ return current frame number """
        return self._frame_number

    def current_duration(self) -> float:
        """ returns current playing duration in sec"""
        return self._frame_number / self._video_meta["framerate"]

    
    def _display_frame(self, event):
        """ displays the frame on the label """

        self.current_imgtk = ImageTk.PhotoImage(self._current_img)
        self.config(image=self.current_imgtk)
