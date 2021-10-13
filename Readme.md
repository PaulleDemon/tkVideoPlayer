# TkVideoplayer

This is a simple library to play video files in tkinter. This library also provides the ability to play , pause, 
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

read the documentation [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/Documentation.md)

#### Sample video player image:
![sample player](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/sample_media_player.png?raw=True)

This example source code can be found [here](https://github.com/PaulleDemon/tkVideoPlayer/blob/master/examples/sample_player.py)


