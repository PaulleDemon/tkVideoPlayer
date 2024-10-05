### Installation
```shell
pip install tkvideoplayer
```

### Quickstart

```py
import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load(r"samplevideo.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

root.mainloop()
```
read additional examples [here](https://github.com/PaulleDemon/tkVideoPlayer/tree/master/examples)

### Methods
TkVideoPlayer inherits from `tk.Label` and display's the image on the label.

Below are the methods of this library.

| Methods          | Parameters                           | Description                                                                                                                                                                                   |
|------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| \_\_init\_\_     | scaled(bool), consistant_frame_rate(bool)=True, keep_aspect(bool)=False, audio(bool)=True   | <br> The scale parameter scales the video to the label size.  <br> The consistant_frame_rate parameter skips frames to keep the framerate consistant. <br> keep_aspect keeps aspect ratio when resizing(note: It will not increase the size)   <br> The audio parameter enables audio in the clip    |
| set_scaled       | scaled(bool), keep_aspect(bool)=False                         | scales the video to the label size.                                                                                                                                                           |
| load             | file_path(str)                       | starts loading the video in a thread.                                                                                                                                                         |
| set_size         | size(Tuple[int, int]), keep_aspect(bool)=False | sets the size of the video frame. setting this will set scaled to `False`                                                                                                                     |
| current_duration  | -                                    | return video duration in seconds.                                                                                                                                                             |
| video_info       | -                                    | returns dictionary containing framerate, framesize, duration.|
| play             | -                                    | Plays the video.                                                                                                                                                                              |
| pause            | -                                    | Pauses the video                                                                                                                                                                              |
| is_paused        | -                                    | returns if the video is currently paused.                                                                                                                                               
| stop             | -                                    | stops playing the file, closes the file.  |
| seek             | sec(int)                             | moves to specific time stamp. provide time stamp in seconds                                           
| keep_aspect             | keep_aspect(bool)                            | keeps aspect ratio when resizing                                          
| metadata         | -                                    | returns meta information of the video if available in the form of dictionary                                           
| mute/unmute      | -                                    | enable/disable audio in the clip |
| set_resampling_method|  method(int)                                   | By default the resampling method while resizing is NEAREST, changing this can affect how its resampled when image is resized, refer PIL documentation to read more (note: this can also affect the framerate of the video)|

### Virtual events

This are events that can be binded to get your desired results

| Virtual event          | Description                                                                                                         |
|------------------------|---------------------------------------------------------------------------------------------------------------------|
| <<Loaded\>\>       | This event is generated when the video file is opened.                                                           |
| <<Duration\>\>       | This event is generated when the video duration is found.                                                           |
| <<SecondChanged\>\>  | This event is generated whenever a second in the video passes (calculated using frame_number%frame_rate==0).        |
| <<FrameGenerated\>\> | This event is generated whenever there is a new frame available. (internal use, don't use this unless you want to). |
| <<Ended\>\>          | This event is generated only when the video has ended.                                                              |

<sub> 

note:

If you would like to draw on the video etc. Copy/fork the repo and instead of inheriting from Label inherit from Canvas.
And use `image_id = self.create_image()` use the image_id to update the image.

</sub>

