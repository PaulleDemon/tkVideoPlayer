# TkVideoplayer

This is a simple library to **play video** files in tkinter. This library also provides the ability to play, pause, 
skip and seek to specific timestamps of the video.

### Installation
```python
pip install tkvideoplayer
```

#### Simple Usage:
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

### read the documentation [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md)

> Please immediately upgrade to the latest version if you are using version 1.3 or below ("pip install tkvideoplayer --upgrade")

### Sample video players made using tkVideoPlayer:
<img src="https://github.com/PaulleDemon/tkVideoPlayer/blob/master/videoplayer_screenshot.png?raw=True" width=500>
<img src="https://user-images.githubusercontent.com/89206401/229363046-36ebcffd-36d2-4c7f-98ce-4aa6b402e9e0.png" width=500)

This example source code can be found [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples)

**Other libraries you might be interested in:**

* [tkstylesheet](https://pypi.org/project/tkstylesheet/) - Helps you style your tkinter application using stylesheets.

* [tkTimePicker](https://pypi.org/project/tkTimePicker/) - An easy-to-use timepicker.

* [PyCollision](https://pypi.org/project/PyCollision/) - Helps you draw hitboxes for 2d games.
