# TkVideoPlayer:

**TkVideoPlayer** inherits from `tk.Label` and display's the image on the label.

Below are the methods of this library.

| Methods          | Parameters                           | Description                                                                                                                                                                                   |
|------------------|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **\_\_init\_\_** | <li>scaled(bool)</li> <li>consistant_frame_rate(bool)</li> <li>keep_aspect(bool)=False</li>   <li>audio(bool)=False</li> | <li>The _scaled_ parameter scales the video to the label size.</li>  <li>The _consistant_frame_rate_ parameter adds an appropriate time delay to keep the framerate consistant.</li> <li>_keep_aspect_ keeps aspect ratio when resizing. (note: It will not increase the size) </li> <li>_audio_ enables audio in clip (experimental)  </li>|
| set_scaled       | <li>scaled(bool)</li> <li>keep_aspect(bool)=False</li> | scales the video to the label size. |
| **load**         | file_path(str)                       | starts loading the video file in a thread.   |
| set_size         | <li>size(Tuple[int, int])</li> <li>keep_aspect(bool)=False</li> | sets the size of the video frame, setting this will set _scaled_ to `False`.  |
| current_duration | -                                   | return the current video duration in seconds. |
| current_frame_number | -                                | get the current number of the frame. |
| **video_info**   | -                                    | returns a dictionary containing name, framerate, framesize, duration, total frames and codec of the video.|
| **play**         | -                                    | Plays the video. |
| **pause**        | -                                    | Pauses the video. |
| **is_paused**    | -                                    | returns if the video is currently paused. |   
| is_stopped       | -                                    | returns if the video is currently stopped. |  
| **stop**         | -                                    | stops playing the file, closes the file. |
| **seek**         | <li>sec(int)</li> <li>any_frame(bool)=False</li> <li>pause(bool)=False</li> | <li>moves to specific time stamp. (provide time stamp in seconds only) </li> <li> any_frame: seek to any nearest keyframe if possible.</li> <li>The _pause_ parameter pauses the video after seeking to the given timestamp.</li> |
| **seek_frame**   | <li>frame(int)</li> <li>delay(float)=False</li> <li>pause(bool)=True</li> | <li>moves to the specific frame number.</li> <li>delay (0-1): add a slight delay while seeking for optimization</li> <li>The _pause_ parameter pauses the video after seeking to the given frame.</li>
| keep_aspect      | keep_aspect(bool)                    | keeps aspect ratio when resizing. |                             
| metadata         | -                                    | returns meta information of the video if available in the form of dictionary. |                             
| set_resampling_method |  method(int)                    | The resampling method while resizing can be set as NEAREST, this can affect how its resampled when image is displayed, refer PIL documentation to read more. (note: this can also affect the framerate of the video) |
| current_img      | -                                    | get the current frame image. |   

### Virtual events:

| Virtual event          | Description                                                                                                         |
|------------------------|---------------------------------------------------------------------------------------------------------------------|
| \<\<Loaded\>\>         | This event is generated when the video file is opened.                                                              |
| \<\<Duration\>\>       | This event is generated when the video duration is found.                                                           |
| \<\<SecondChanged\>\>  | This event is generated whenever a second in the video passes (calculated using frame_number%frame_rate==0).        |
| \<\<FrameChanged\>\>   | This event is generated whenever there is a new frame available.                                                    |
| \<\<Ended\>\>          | This event is generated only when the video has ended.                                                              |

<sub> 

Note:

If you would like to draw on the video etc. Copy/fork the repo and instead of inheriting from Label inherit from Canvas.
  
And add `image_id = self.create_image()` and then use the image_id to update the image.

</sub>

