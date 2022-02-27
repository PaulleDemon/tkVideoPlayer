# TkVideoPlayer:

TkVideoPlayer inherits from `tk.Label` and display's the image on the label.

Below are the methods of this library.

| Methods          | Parameters                           | Description                                                                                                                                                                                   |
|------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| \_\_init\_\_     | scaled(bool), pre_load(bool)=False   | The scale parameter scales the video to the label size.  The pre_load parameter loads the video to memory first then plays  (pre_load not recommended for large videos, keep it False).       |
| set_scaled       | -                                    | scales the video to the label size.                                                                                                                                                           |
| load             | file_path(str), pre_load(bool)=False | starts loading the video in a thread.                                                                                                                                                         |
| loaded           | -                                    | returns `True` if the video has been loaded to memory.                                                                                                                                        |
| set_size         | size(Tuple[int, int])                | sets the size of the video frame. setting this will set scaled to `False`                                                                                                                     |
| duration         | -                                    | return video duration in seconds.                                                                                                                                                             |
| frame_size       | -                                    | returns the original dimension of the video.                                                                                                                                                  |
| frame_rate       | -                                    | returns the frame rate of the video.                                                                                                                                                          |
| frame_info       | -                                    | returns `tuple` containing current number of frames, frame image, current frame number  and frame rate.                                                                                       |
| play             | -                                    | Plays the video.                                                                                                                                                                              |
| pause            | -                                    | Pauses the video                                                                                                                                                                              |
| is_paused        | -                                    | returns if the video is currently paused.                                                                                                                                                     |
| stop             | -                                    | stops the video and removes the video from memory. If you want to load a new video use `load` directly `stop` is not required in that case. If stop is called, you will have to reload file.  |
| seek             | time_stamp(float)                    | moves to specific time stamp. provide time_stamp in seconds                                                                                                                                   |
| skip_sec         | sec(int)                             | skips by few seconds. If you want to skip -5 sec provide -5 as argument.                                                                                                                      |
| skip_frames      | number_of_frames(int)                | skips specific number of frames.                                                                                                                                                              |
| current_duration | -                                    | return's current duration of the video                                                                                                                                                        |


### Virtual events:

| Virtual event          | Description                                                                                                         |
|------------------------|---------------------------------------------------------------------------------------------------------------------|
| \<\<loaded\>\>         | This event is generated when all the frames has been loaded into the memory.                                        |
| \<\<Duration\>\>       | This event is generated when the video duration is found.                                                           |
| \<\<SecondChanged\>\>  | This event is generated whenever a second in the video passes (calculated using frame_number%frame_rate==0).        |
| \<\<FrameGenerated\>\> | This event is generated whenever there is a new frame available. (internal use, don't use this unless you want to). |
| \<\<Ended\>\>          | This event is generated only when the video has ended.                                                              |

<sub> 

note:

If you would like to draw on the video etc. Copy/fork the repo and instead of inheriting from Label inherit from Canvas.
And use `image_id = self.create_image()` use the image_id to update the image.

</sub>

> Note: Loading large files can be slow and might have lag
