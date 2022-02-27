# TkVideoplayer

This is a simple library to play video files in tkinter. This library also provides the ability to play, pause, 
skip and seek specific frames.

#### Example:
```python
import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

videoplayer = TkinterVideo(master=root, scaled=True, pre_load=False)
videoplayer.load(r"samplevideo.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

root.mainloop()
```

> Note: the master argument has to be explicitly set, you cannot use `TkinterVideo(root)`, 
> instead you must use `TkinterVideo(master=root)`.

read the documentation [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md)

#### Sample video player made using tkVideoPlayer:
![Sample player](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/videoplayer_screenshot.png?raw=True)

This example source code can be found [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py)


**Other libraries you might be interested in:**

* [tkstylesheet](https://pypi.org/project/tkstylesheet/) - helps you style your tkinter application using stylesheets.

* [tkTimePicker](https://pypi.org/project/tkTimePicker/) - an easy-to-use timepicker.

* [PyCollision](https://pypi.org/project/PyCollision/) - helps you draw hitboxes for 2d games