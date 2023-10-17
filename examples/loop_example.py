import tkinter as tk
from tkVideoPlayer import TkinterVideo


def loop(e):
    # if the video had ended then replays the video from the beginning
    tkvideo.play()


root = tk.Tk()

tkvideo = TkinterVideo(scaled=True, master=root)
tkvideo.load(r"test.mp4")
tkvideo.pack(expand=True, fill="both")
tkvideo.play() # play the video
tkvideo.bind("<<Ended>>", loop) # when the video ends calls the loop function
root.mainloop()
