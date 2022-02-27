import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

tkvideo = TkinterVideo(scaled=False, pre_load=False, master=root)
tkvideo.load(r"../sampledata/samplevideo.mp4")
tkvideo.pack(expand=True, fill="both")
tkvideo.set_size((1200, 600))
tkvideo.play() # play the video

root.mainloop()