import tkinter as tk
from tkinter import filedialog
from tkmultimedia import TkinterVideo


def load_video():
    file_path = filedialog.askopenfilename()
    print(file_path)
    if file_path:
        vid_player.load(file_path)


def play_pause():

    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


root = tk.Tk()

load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack()

play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

vid_player = TkinterVideo(master=root, scaled=True, pre_load=False)
vid_player.pack(expand=True, fill="both")

root.mainloop()