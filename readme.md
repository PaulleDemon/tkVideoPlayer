# Tkinter media player

This is a simple library to play video files. This library also provides the ability to play , pause, 
skip and seek specific frames.

```python
root = tk.Tk()

tkvideo = TkinterVideo(master=root, scaled=False, pre_load=False)
tkvideo.load(r"samplevideo.mp4")
tkvideo.pack(expand=True, fill="both")

tkvideo.play() # play the video

root.mainloop()
```

read the documentation [here]()