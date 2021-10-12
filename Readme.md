# TkVideoplayer

This is a simple library to play video files in tkinter. This library also provides the ability to play , pause, 
skip and seek specific frames.

#### Example:
```python
import tkinter as tk
from tkVideoPlayer import TkinterVideo
root = tk.Tk()

tkvideo = TkinterVideo(master=root, scaled=False, pre_load=False)
tkvideo.load(r"samplevideo.mp4")
tkvideo.pack(expand=True, fill="both")

tkvideo.play() # play the video

root.mainloop()
```

read the documentation [here](https://github.com/PaulleDemon/tkmultimedia/blob/master/Documentation.md)

#### Sample video player image:
![sample player](https://github.com/PaulleDemon/tkmultimedia/blob/master/sample_media_player.png)

This example source code can be found [here](https://github.com/PaulleDemon/tkmultimedia/blob/master/examples/sample_player.py)


