import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()

tkvideo = TkinterVideo(scaled=False, master=root)
tkvideo.load(r"VID_20190928_063807.mp4")
tkvideo.pack(expand=True, fill="both")
tkvideo.set_size((1200, 600)) # sets the frame size
tkvideo.play() # play the video

tkvideo.bind("<<Loaded>>", lambda e: print(tkvideo.metadata())) # prints the meta information
tkvideo.bind("<<Loaded>>", lambda e: print(tkvideo.video_info()), add='+') # prints duration frame rate and frame size

root.mainloop()