# TkVideoPlayer:

TkVideoPlayer inherits from `tk.Label` and display's the image on the label.

Below are the methods of this library.

| Methods          | Parameters                           | Description                                                                                                                                                                                   |
|------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| \_\_init\_\_     | scaled(bool), consistant_frame_rate(bool)=True   | The scale parameter scales the video to the label size.  The consistant_frame_rate parameter skips frames to keep the framerate consistant       |
| set_scaled       | -                                    | scales the video to the label size.                                                                                                                                                           |
| load             | file_path(str), pre_load(bool)=False | starts loading the video in a thread.                                                                                                                                                         |
| set_size         | size(Tuple[int, int])                | sets the size of the video frame. setting this will set scaled to `False`                                                                                                                     |
| current_duration  | -                                    | return video duration in seconds.                                                                                                                                                             |
| video_info       | -                                    | returns dictionary containing framerate, framesize, duration.|
| play             | -                                    | Plays the video.                                                                                                                                                                              |
| pause            | -                                    | Pauses the video                                                                                                                                                                              |
| is_paused        | -                                    | returns if the video is currently paused.                                                                                                                                               
| stop             | -                                    | stops playing the file, closes the file.  |
| seek             | time_stamp(int)                    | moves to specific time stamp. provide time_stamp in seconds                                           
| metadata         | -                                  | returns meta information of the video if available in the form of dictionary                                           

### Virtual events:

| Virtual event          | Description                                                                                                         |
|------------------------|---------------------------------------------------------------------------------------------------------------------|
| \<\<Loaded\>\>       | This event is generated when the video file is opened.                                                           |
| \<\<Duration\>\>       | This event is generated when the video duration is found.                                                           |
| \<\<SecondChanged\>\>  | This event is generated whenever a second in the video passes (calculated using frame_number%frame_rate==0).        |
| \<\<FrameGenerated\>\> | This event is generated whenever there is a new frame available. (internal use, don't use this unless you want to). |
| \<\<Ended\>\>          | This event is generated only when the video has ended.                                                              |

<sub> 

note:

If you would like to draw on the video etc. Copy/fork the repo and instead of inheriting from Label inherit from Canvas.
And use `image_id = self.create_image()` use the image_id to update the image.

</sub>

