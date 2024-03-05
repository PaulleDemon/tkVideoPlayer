# Modified version of TkVideoPlayer by Akascape

import av
import pyaudio
import time
import threading
import logging
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
from typing import Tuple, Dict

logging.getLogger('libav').setLevel(logging.CRITICAL)  # removes warning: deprecated pixel format used

class TkinterVideo(tk.Label):

    def __init__(self, master, scaled: bool = True, consistant_frame_rate: bool = True, keep_aspect: bool = False, audio=True, *args, **kwargs):
        super(TkinterVideo, self).__init__(master, *args, **kwargs)

        self.path = ""
        self._load_thread = None
        self._paused = True
        self._stop = True
        self.consistant_frame_rate = consistant_frame_rate # tries to keep the frame rate consistant by delaying between frames
        self._container = None
        self._current_img = None
        self._current_frame_Tk = None
        
        self._frame_number = 0
        self._time_stamp = 0
        self._current_frame_size = (0, 0)
        self._seek = False
        self._seek_sec = 0
        self._seek_frame = False
        self._frame = 0
        self._any_frame = False
        self._seek_pause = False
        self._audio = audio
        
        self._video_info = {
            "name": None, # name/path of the video
            "duration": 0, # duration of the video
            "framerate": 0, # frame rate of the video
            "framesize": (0, 0), # tuple containing frame height and width of the video
            "frames": 0, # total frames of the video
            "codec": None # codec of the file
        }   

        self.set_scaled(scaled)
        self._keep_aspect_ratio = keep_aspect
        self._resampling_method: int = Image.NEAREST

        self.bind("<<Destroy>>", self.stop)
        self.bind("<<FrameGenerated>>", self._display_frame)
    
    def keep_aspect(self, keep_aspect: bool):
        """ keeps the aspect ratio when resizing the image """
        self._keep_aspect_ratio = keep_aspect

    def set_resampling_method(self, method: int):
        """ sets the resampling method when resizing """
        self._resampling_method = method

    def set_size(self, size: Tuple[int, int], keep_aspect: bool=False):
        """ sets the size of the video """
        self.set_scaled(False, self._keep_aspect_ratio)
        self._current_frame_size = size
        self._keep_aspect_ratio = keep_aspect

    def _resize_event(self, event):
        """ scales the label frame dynamically """
        self._current_frame_size = event.width, event.height

        if self._paused and self._current_img and self.scaled:
            if self._keep_aspect_ratio:
                proxy_img = ImageOps.contain(self._current_img.copy(), self._current_frame_size)

            else:
                proxy_img = self._current_img.copy().resize(self._current_frame_size)
            
            self._current_imgtk = ImageTk.PhotoImage(proxy_img)
            self.config(image=self._current_imgtk)

    def set_scaled(self, scaled: bool, keep_aspect: bool = False):
        """ set dynamic scalling for the label """
        self.scaled = scaled
        self._keep_aspect_ratio = keep_aspect

        if scaled:
            self.bind("<Configure>", self._resize_event)

        else:
            self.unbind("<Configure>")
            self._current_frame_size = self.video_info()["framesize"]

    def _set_frame_size(self, event=None):
        """ sets frame size to avoid unexpected resizing """
        self._video_info["framesize"] = (self._container.streams.video[0].width, self._container.streams.video[0].height)

        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._video_info["framesize"], (255, 0, 0, 0)))
        self.config(width=150, height=100, image=self.current_imgtk)
        
    def _display_frame(self, event):
        """ displays the frame on the label """

        self.event_generate("<<FrameChanged>>")

        if self.scaled or (len(self._current_frame_size) == 2 and all(self._current_frame_size)):
            
            if self._keep_aspect_ratio:
                self._current_img = ImageOps.contain(self._current_img, self._current_frame_size, self._resampling_method)

            else:
                self._current_img =  self._current_img.resize(self._current_frame_size, self._resampling_method)

        else:
            self._current_frame_size = self.video_info()["framesize"] if all(self.video_info()["framesize"]) else (1, 1)
            
            if self._keep_aspect_ratio:
                self._current_img = ImageOps.contain(self._current_img, self._current_frame_size, self._resampling_method)

            else:
                self._current_img =  self._current_img.resize(self._current_frame_size, self._resampling_method)
        
        self.current_imgtk = ImageTk.PhotoImage(self._current_img)
        self.config(image=self.current_imgtk)
        
    def _load(self, path):
        """ load's file from a thread """

        current_thread = threading.current_thread()

        with av.open(path, "r") as self._container:

            self._container.streams.video[0].thread_type = "AUTO"
            
            self._container.fast_seek = True
            self._container.discard_corrupt = True

            stream = self._container.streams.video[0]

            try:
                if self._audio:
                    audio_stream = self._container.streams.audio[0]

                    samplerate = audio_stream.rate # this will work as the video clock
                    channels = audio_stream.channels
              
                    p = pyaudio.PyAudio()
                    audio_stream = p.open(format=pyaudio.paFloat32,
                                    channels=channels,
                                    rate=samplerate,
                                    output=True)
                    self.audio_stream_base = self._container.streams.audio[0].time_base
                else:
                    audio_stream = False
            except:
                audio_stream = False
                
            self._video_info["framerate"] = int(stream.average_rate)
            self._video_info["frames"] = int(stream.frames)
            self._video_info["codec"] = str(stream.codec_context.name)
            self._video_info["name"] = str(stream.container.name)
    
            self.video_stream_base = stream.time_base
            
            try:              
                self._video_info["duration"] = round(float(stream.duration * self.video_stream_base), 2)
                self.event_generate("<<Duration>>")  # duration has been found

            except (TypeError, tk.TclError):  # the video duration cannot be found, this can happen for mkv files
                pass

            self._frame_number = 0

            self._set_frame_size()

            try:
                self.event_generate("<<Loaded>>") # generated when the video file is opened
            
            except tk.TclError:
                pass

            now = time.time_ns() // 1_000_000  # time in milliseconds
            then = now
            time_in_frame = (1/self._video_info["framerate"])*1000 # second it should play each frame
            
            self.frame_buffers = []

            while self._load_thread == current_thread and not self._stop:
                
                if self._seek: # seek to nearest timestamp (second)
                    self._container.seek(self._seek_sec*1000000 , whence='time', backward=True, any_frame=self._any_frame) # the seek time application is to correct the frame
                    self._seek = False
                    self._frame_number = self._video_info["framerate"] * self._seek_sec
                    self._seek_sec = 0
                    
                    if self._seek_pause:
                        self.play()
                        self.after(50, self.pause)
                        
                if self._seek_frame: # seek to a specific frame               
                    sec = int(self._frame/self._video_info["framerate"]) # get average timestamp of that required frame
                    self._container.seek(sec*1000000, whence='time', backward=True) # then seek to the nearest timestamp/keyframe
                    frame = next(self._container.decode(video=0)) # get the next frame
                    sec_frame = int(frame.pts * self.video_stream_base * self._video_info["framerate"]) # get that keyframe number
                    
                    try:
                        if self._delay: # a little bit delay can limit the cpu usage
                            time.sleep(self._delay)
                            
                        # seek to the required frame
                        for _ in range(sec_frame, self._frame):
                            frame = next(self._container.decode(video=0))

                        self._current_img = frame.to_image()
                        self._time_stamp = round(float(frame.pts * self.video_stream_base), 2)
                        self._frame_number = self._frame
                        self.event_generate("<<FrameGenerated>>")
                        self._seek_frame = False
                        self._frame = 0
                        
                        if self._seek_pause:
                            self.pause()
                            
                    except (StopIteration, av.error.EOFError, tk.TclError):
                        self._seek_frame = False
                        self._frame = 0
                        break
                    
                if self._paused:
                    time.sleep(0.0001) # to allow other threads to function better when its paused
                    continue
                
                now = time.time_ns() // 1_000_000  # time in milliseconds
                delta = now - then  # time difference between current frame and previous frame
                then = now
                af = 0
                dont_loop = False
                
                try:
                    if audio_stream and self._audio:
                        last_audio_buffer = False
                        last_video_buffer = False
                        
                        while True:
                            frame = next(self._container.decode(video=0, audio=0))
                            
                            if 'Video' in repr(frame):
                                if last_audio_buffer:
                            
                                    if round(float(frame.pts * self.video_stream_base), 2)<=last_audio_buffer:
                                        self.frame_buffers.append(frame)
                                    else:
                                        break # break if the last audio buffer pts matches the final video buffer pts
                                    if not last_video_buffer:
                                        break
                                    if af<=3:
                                        break
                                    if af>=100: # avoid leakage
                                        self.frame_buffers = []
                                        self.stop()
                                        break
                                    dont_loop = True
                                else:
                                    self.frame_buffers.append(frame)
                                    last_video_buffer = round(float(frame.pts * self.video_stream_base), 2)
                                    
                            else:
                                if dont_loop: # avoid excessive buffering, can cause stutters
                                    break
                                self.frame_buffers.append(frame)
                                last_audio_buffer = round(float(frame.pts * self.audio_stream_base), 2)
                                af+=1
                
                        # sort all the frames based on their presentation time
                        self.frame_buffers = sorted(self.frame_buffers, key=lambda f:f.pts*self.video_stream_base if 'Video' in repr(f) else f.pts*self.audio_stream_base)
                                
                        for i in self.frame_buffers:
                            if 'Video' in repr(i):
               
                                self._current_img = i.to_image()
                                self._frame_number += 1
                                    
                                self.event_generate("<<FrameGenerated>>")

                                if self._frame_number % self._video_info["framerate"] == 0:
                                    self.event_generate("<<SecondChanged>>")
                                                
                            elif self._audio:
                                self._time_stamp = round(float(i.pts * self.audio_stream_base), 2)
                                
                                audio_data = i.to_ndarray().astype('float32')
                                interleaved_data = audio_data.T.flatten().tobytes()
                                audio_stream.write(interleaved_data)
                            if self._paused:
                                break
                            if self._stop:
                                break
                       
                    else:
                        frame = next(self._container.decode(video=0))
                        
                        self._time_stamp = round(float(frame.pts * self.video_stream_base), 2)
         
                        self._current_img = frame.to_image()
                        self._frame_number += 1
                    
                        self.event_generate("<<FrameGenerated>>")

                        if self._frame_number % self._video_info["framerate"] == 0:
                            self.event_generate("<<SecondChanged>>")

                        if self.consistant_frame_rate:             
                            time.sleep(max((time_in_frame - delta)/1000, 0))
                                
                    self.frame_buffers = [] # flush the buffers
                    
                except (StopIteration, av.error.EOFError, tk.TclError):
                    break

        self._frame_number = 0
        self._paused = True
        self._load_thread = None
        self._container = None
        self.frame_buffers = []
        frame = None
        stream = None
    
        if audio_stream:
            audio_stream.stop_stream()
            audio_stream.close()
            p.terminate()

        try:
            self.event_generate("<<Ended>>")  # this is generated when the video ends
        
        except tk.TclError:
            pass
                   
    def load(self, path: str):
        """ loads the file from the given path """
        self.stop()
        self.path = path
        self._load_thread = None
        self._container = None
        self.frame_buffers = []
        
    def stop(self):
        """ stops reading the file from reading """
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
            self._load_thread = threading.Thread(target=self._load,  args=(self.path, ), daemon=True)
            self._load_thread.start()

    def is_paused(self):
        """ returns if the video is paused """
        return self._paused

    def is_stopped(self):
        """ returns if the video is stopped """
        return self._stop

    def video_info(self) -> Dict:
        """ returns dict containing basic information about the video """
        return self._video_info

    def metadata(self) -> Dict:
        """ returns metadata if available """
        if self._container:
            return self._container.metadata

        return {}

    def mute(self) -> None:
        self._audio = False

    def unmute(self) -> None:
        self._audio = True
             
    def current_frame_number(self) -> int:
        """ return current frame number """
        return self._frame_number

    def current_duration(self) -> float:
        """ returns current playing duration in sec """
        return self._time_stamp
    
    def current_img(self) -> Image:
        """ returns current frame image """
        return self._current_img
        
    def seek(self, sec: int,  any_frame: bool = False, pause: bool = False):
        """ seeks to specific time (not accurate) """ 
        self._seek = True
        self._seek_sec = sec
        self._any_frame = any_frame
        self._seek_pause = pause
        
    def seek_frame(self, frame: int, pause: bool = True, delay: float = 0.3):
        """ seeks to specific frame (accurate) """        
        self._seek_frame = True
        self._frame = frame
        self._seek_pause = pause
        self._delay = delay if int(delay)<1 else 1.0
