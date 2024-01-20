import customtkinter
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import os, datetime

def open_video():
    vid_player.stop()
    global video_file
    new_video_file = filedialog.askopenfilename(filetypes =
                                                [('Video', ['*.mp4','*.avi','*.mov','*.mkv']),
                                                 ('All Files', '*.*')])
    if new_video_file:
        video_file = new_video_file
        vid_player.load(video_file)
        vid_player.play()
        progress_slider.set(-1)
        play_pause_btn.configure(text="Pause II")

def seek(value):
    if video_file:
        vid_player.seek_frame(int(value), pause=True, delay=0.0)
        play_pause_btn.configure(text="Play")
        
def play_pause():
    if video_file:
        if vid_player.is_paused():
            vid_player.play()
            play_pause_btn.configure(text="Pause II")            
        else:
            vid_player.pause()
            play_pause_btn.configure(text="Play")
            
def update_scale(event):    
    progress_slider.set(int(vid_player.current_frame_number()))
    current_duration = datetime.timedelta(seconds=int(vid_player.current_duration()))
    label_1.configure(text=str(current_duration))
            
def update_duration(event):
    button_1.configure(text=os.path.basename(vid_player.video_info()["name"]))
    total_frames = int(vid_player.video_info()["frames"])
    progress_slider.configure(to=total_frames, number_of_steps=total_frames)
    duration = int(vid_player.video_info()["duration"])
    label_2.configure(text=str(datetime.timedelta(seconds=duration)))
    
def video_ended(event):
    play_pause_btn.configure(text="Play")
    progress_slider.set(0)
    label_1.configure(text="0:00:00")
    # vid_player.play() # loop video if required
    
customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x500")
app.title("CustomTkinter x TkVideoPlayer.py")

video_file = ''
frame_1 = customtkinter.CTkFrame(master=app, corner_radius=15)
frame_1.pack(pady=20, padx=20, fill="both", expand=True)

button_1 = customtkinter.CTkButton(master=frame_1, text="Open Video", corner_radius=8, command=open_video)
button_1.pack(pady=10, padx=10, fill="both")

vid_player = TkinterVideo(master=frame_1, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg="black")
vid_player.set_resampling_method(0)
vid_player.pack(expand=True, fill="both", padx=10, pady=10)
vid_player.bind("<<Ended>>", video_ended )
vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<FrameChanged>>", update_scale)

progress_slider = customtkinter.CTkSlider(master=frame_1, from_=0, to=1, number_of_steps=1, command=seek)
progress_slider.set(1)
progress_slider.pack(fill="both", padx=10, pady=10)

label_1 = customtkinter.CTkLabel(master=frame_1, text="0:00:00")
label_1.pack(side="left", padx=20, anchor="n")

label_2 = customtkinter.CTkLabel(master=frame_1, text="0:00:00")
label_2.pack(side="right", padx=20, anchor="n")

play_pause_btn = customtkinter.CTkButton(master=frame_1, text="Play", command=play_pause, width=10)
play_pause_btn.pack(pady=10)

app.mainloop()
