# TkVideoplayer

This is a simple library to play video files in tkinter. This library also provides the ability to play, pause, 
skip and seek to specific timestamps.

#### Example:
```python
import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load(r"samplevideo.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

root.mainloop()
```

read the documentation [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md)

you can easily integrate this with **CustomTkinter** as well: refer [How to integrate with CustomTkinter?](https://github.com/PaulleDemon/tkVideoPlayer/discussions/23#discussioncomment-4475005)

> Please immediately upgrade to the latest version if you are using version 1.3 or below


#### Sample video player made using tkVideoPlayer:
![Sample player](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/videoplayer_screenshot.png?raw=True)



> Note the above is a video player made using this library. The UI doens't come along with the library. Refer example on how to build the video player [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py)

**Other libraries you might be interested in:**

* [tkstylesheet](https://pypi.org/project/tkstylesheet/) - Helps you style your tkinter application using stylesheets.

* [tkTimePicker](https://pypi.org/project/tkTimePicker/) - An easy-to-use timepicker.

* [PyCollision](https://pypi.org/project/PyCollision/) - Helps you draw hitboxes for 2d games.


