import tkinter as tk
from tkVideoPlayer import TkinterVideo


root = tk.Tk()

tkvideo = TkinterVideo(scaled=True, master=root, loop=True)
# tkvideo.loop = True # can also set loop value after initialization
# tkvideo.loop(True) # alternative
tkvideo.load(r"sample_m4v.m4v")
tkvideo.pack(expand=True, fill="both")
tkvideo.play() # play the video
root.mainloop()
