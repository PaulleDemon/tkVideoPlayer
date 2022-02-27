import av
import time
import threading
import logging
import tkinter as tk
from PIL import ImageTk, Image
from typing import Tuple

logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used, make sure you


# did set range correctly


class TkinterVideo(tk.Label):

    def __init__(self, scaled: bool = True, pre_load: bool = False, *args, **kwargs):
        super(TkinterVideo, self).__init__(*args, **kwargs)

        self.preload = pre_load

        self.image_sequence = []
        self.current_imgtk = None
        self.current_img = None
        self.load_thread = None

        self._frame_rate = 1
        self._frame_size = (100, 75)
        self._frame_number = 0

        self._current_size = ()
        self.scaled = scaled

        self._video_duration = 0
        self._video_frame_length = 0  # number of frames in the video
        self._playing_thread = None  # thread in which the video is being loaded
        self._loaded = False
        self._paused = True
        self._playing = False
        self._stopped = False

        self.set_scaled(scaled)

        self.bind("<Destroy>", lambda _: self.stop())  # stop the thread when the user closes or destroys the player

    def set_scaled(self, scaled: bool):
        self.scaled = scaled

        if scaled:
            self.bind("<Configure>", self._resize_event)

        else:
            self.unbind("<Configure>")

    def set_size(self, size: Tuple[int, int]):
        """ sets the size of the video """
        self.set_scaled(False)
        self._current_size = size

    def _resize_event(self, event):

        self._current_size = event.width, event.height

        if self._paused and self.current_img and self.scaled:
            self.current_img = self.image_sequence[self._frame_number].copy().resize(self._current_size)
            self.current_imgtk = ImageTk.PhotoImage(self.current_img)
            self.config(image=self.current_imgtk)

    def _set_frame_size(self, event=None):
        """ sets frame size to avoid unexpected resizing """
        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._frame_size, (255, 0, 0, 0)))
        self.config(width=150, height=100, image=self.current_imgtk)

    def _load(self, file_path: str):
        """ loads the frames from a thread """
        self.image_sequence = []
        current_thread = threading.current_thread()

        try:
            with av.open(file_path) as container:

                try:
                    self._frame_rate = int(container.streams.video[0].average_rate)
                except TypeError:
                    raise TypeError("Not a video file")

                self._frame_size = (container.streams.video[0].width, container.streams.video[0].height)

                try:
                    self._video_duration = float(
                        container.streams.video[0].duration * container.streams.video[0].time_base)

                except TypeError:  # the video duration cannot be found, this can happen for mkv files
                    pass

                self.event_generate("<<Duration>>")  # duration has been found

                self._video_frame_length = container.streams.video[0].frames

                if self.scaled:
                    self._set_frame_size()

                if self.preload:
                    self.image_sequence = [frame.to_image() for frame in container.decode(video=0)]

                else:

                    for frame in container.decode(video=0):  # container.decode yields generator

                        if self.load_thread != current_thread or self._stopped:
                            return

                        self.image_sequence.append(frame.to_image()) # if memory error try setting height and with expcitily, refer pyav docs, to_image()

            self._loaded = True

            self.event_generate("<<loaded>>")

        except Exception as e:
            raise e

    def load(self, file_path="", pre_load: bool = False):
        """ loads the video and generates <<loaded>> event after loading """
        self.preload = pre_load
        self.stop()
        self._stopped = False
        self.load_thread = threading.Thread(target=self._load, args=(file_path,), daemon=True)
        self.load_thread.start()

    def loaded(self) -> bool:
        """ returns whether the video has been loaded """
        return self._loaded

    def duration(self) -> int:
        """ returns video duration """
        return self._video_duration

    def frame_size(self) -> Tuple[int, int]:
        """ return frame dimension """
        return self._frame_size

    def frame_rate(self) -> float:
        """ returns the current frame rate """
        return self._frame_rate

    def frame_info(self) -> Tuple[int, tk.Image, int, float]:
        """ return number of frames, current frame image, frame number and frame rate  """
        return self._video_frame_length, self.current_img, self._frame_number, self._frame_rate

    def play(self):
        """ plays the loaded video """

        self._paused = False
        self._stopped = False
        if self._frame_number == len(self.image_sequence):
            self._frame_number = 0

        self.bind("<<FrameGenerated>>", self._display_frame)

        if not self.preload and not self._playing:
            self._playing = True
            self._playing_thread = threading.Thread(target=self._update_frames, daemon=True)
            self._playing_thread.start()

        elif self.preload and not self._playing:
            self._paused = True
            self.bind("<<loaded>>", self._start_loaded)

    def _start_loaded(self, event):

        self._paused = False
        if not self._playing:
            self._stopped = False
            self._playing = True
            self._playing_thread = threading.Thread(target=self._update_frames, daemon=True)
            self._playing_thread.start()

    def is_paused(self) -> bool:
        """ returns if the video is paused """
        return self._paused

    def pause(self):
        """ pauses the video """
        self._paused = True

    def stop(self):
        """ stop removes the loaded video and reset the frame_number """
        self._playing = False
        self._paused = True
        self._frame_number = 0
        self.image_sequence = []
        self._loaded = False
        self._stopped = True

    def seek(self, time_stamp: float):

        if 0 < time_stamp < self._video_duration:
            self._frame_number = time_stamp * self._frame_rate

    def skip_sec(self, sec: int):
        """ skip by seconds """
        if 0 < self._frame_number + (sec * self._frame_rate) < self._video_frame_length:
            self._frame_number = self._frame_number + (sec * self._frame_rate)

        elif self._frame_number + (sec * self._frame_rate) < 0:
            self._frame_number = 0

        elif self._frame_number + (sec * self._frame_rate) > self._video_frame_length:
            self._frame_number = self._video_frame_length - 1

    def skip_frames(self, number_of_frames: int):
        """ skip by how many frames +ve or -ve """

        if number_of_frames < 0 and (self._frame_number - number_of_frames) > 0:
            self._frame_number -= number_of_frames

        elif number_of_frames > 0 and (self._frame_number + number_of_frames) > len(self.image_sequence):
            self._frame_number += number_of_frames

    def current_duration(self) -> float:
        """ returns current playing duration in sec"""
        return self._frame_number / self._frame_rate

    def _update_frames(self):
        """ updates frame from thread """

        now = time.time_ns() // 1_000_000  # time in milliseconds
        then = now

        while self._playing:

            if self._loaded and self._frame_number >= len(self.image_sequence) - 1:
                break

            if not self._paused and self._frame_number < len(self.image_sequence) - 1:

                now = time.time_ns() // 1_000_000  # time in milliseconds
                delta = now - then  # time difference between current frame and previous frame
                then = now

                self.current_img = self.image_sequence[self._frame_number].copy()

                if self.scaled or len(self._current_size) == 2:
                    self.current_img = self.current_img.resize(self._current_size)

                if self._stopped: # if the player has been stopped return
                    return

                self.event_generate("<<FrameGenerated>>")

                self._frame_number += 1

                if self._frame_number % self._frame_rate == 0:
                    self.event_generate("<<SecondChanged>>")

                if delta / 1000 >= 1 / self._frame_rate:
                    continue

                time.sleep((1 / self._frame_rate) - (delta / 1000))  # sleep to correct the fps
                continue

            if not self._loaded:
                time.sleep(0.0020)

        self._frame_number = 0
        self._playing = False
        self._paused = True

        self.event_generate("<<Ended>>")  # this is generated when the video ends

    def _display_frame(self, event):
        """ updates the image in the label """

        self.current_imgtk = ImageTk.PhotoImage(self.current_img)
        self.config(image=self.current_imgtk)
