import tkinter as tk
import random
import time
import threading
import vlc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import requests

# RTSP URL
RTSP_URL = "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"

# Function to start VLC player in a separate thread
def start_vlc_player():
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(RTSP_URL)
    player.set_media(media)
    player.set_xwindow(video_frame.winfo_id())  # Linux specific
    player.play()
    while True:
        time.sleep(1)

# Function to update the graph based on sensor data
def update_graph():
    while True:
        # Random data for simulation, replace with actual sensor data
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        points.append([x, y])
        ax.clear()
        ax.plot(*zip(*points), marker='o', markersize=2, color='red')
        ax.fill(*zip(*points), 'yellow', alpha=0.3)
        canvas.draw()
        time.sleep(0.1)

# Function to update analog gauges
def update_gauges():
    while True:
        for gauge in gauges:
            value = random.uniform(0, 100)
            gauge.set_value(value)
        time.sleep(1)

# Function to update accelerometer and gyroscope display
def update_acc_gyro():
    while True:
        accel_value = random.uniform(-10, 10)
        gyro_value = random.uniform(-180, 180)
        pitch_roll_canvas.update_labels(accel_value, gyro_value)
        time.sleep(1)

# Function to update status indicators
def update_status():
    while True:
        power_status.update_status(random.choice([True, False]))
        pump_status.update_status(random.choice([True, False]))
        misc_status.update_status(random.choice([True, False]))
        time.sleep(2)

# Custom gauge class
class Gauge(tk.Canvas):
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.value = 0
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.create_rectangle(10, 10, self.width-10, self.height-10, outline="black", fill="lime green", width=2)
        self.create_text(self.width // 2, self.height // 2, text="Amp", font=("Arial", 14, "bold"))
        self.draw_scale()

    def draw_scale(self):
        scale_values = [1, 5, 15, 20, 25, 30]
        scale_length = self.width - 20
        scale_step = scale_length / (len(scale_values) - 1)

        for i, value in enumerate(scale_values):
            x = 10 + i * scale_step
            self.create_line(x, self.height - 10, x, self.height - 20, fill="black")
            self.create_text(x, self.height - 5, text=str(value), anchor=tk.CENTER)
    
    def set_value(self, value):
        self.value = value
        angle = (value / 100) * 180
        x = self.width // 2 + (self.width // 2 - 20) * np.cos(np.radians(180 - angle))
        y = self.height // 2 - (self.height // 2 - 20) * np.sin(np.radians(180 - angle))
        self.coords(self.arrow, self.width // 2, self.height // 2, x, y)

# Custom pitch and roll class
class PitchRoll(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.create_arc((10, 10, self.width-10, self.height-10), start=0, extent=180, fill="sky blue", outline="black", width=2)
        self.create_arc((10, 10, self.width-10, self.height-10), start=180, extent=180, fill="green", outline="black", width=2)
        self.accel_label = self.create_text(self.width // 2, self.height // 4, text="Accelerometer: 0.00", fill="white", font=("Arial", 12))
        self.gyro_label = self.create_text(self.width // 2, 3 * self.height // 4, text="Gyroscope: 0.00", fill="white", font=("Arial", 12))
    
    def update_labels(self, accel_value, gyro_value):
        self.itemconfig(self.accel_label, text=f"Accelerometer: {accel_value:.2f}")
        self.itemconfig(self.gyro_label, text=f"Gyroscope: {gyro_value:.2f}")

# Custom LED status indicator class
class LedStatus(tk.Canvas):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, **kwargs)
        self.label = label
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.led = self.create_oval(10, 10, self.width-10, self.height-10, fill="dark grey", outline="black", width=2)
        self.label_text = self.create_text(self.width // 2, self.height - 20, text=label, font=("Arial", 12))
    
    def update_status(self, status):
        color = "yellow" if status else "dark grey"
        self.itemconfig(self.led, fill=color)

# Function to toggle fullscreen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Main application
root = tk.Tk()

# Define grid weights for rows and columns
#root.grid_rowconfigure(0, weight=5)  # Top row
#root.grid_rowconfigure(1, weight=2)  # Middle row
#root.grid_rowconfigure(2, weight=3)  # Bottom row
#root.grid_columnconfigure(0, weight=1)
#root.grid_columnconfigure(1, weight=1)

# Video widget
video_frame = tk.Frame(root, width=800, height=600, bd=0, relief="solid")
video_frame.grid(row=0, column=0, rowspan=2, sticky='nsew')

# Check if RTSP URL is accessible
try:
    response = requests.get(RTSP_URL)
    if response.status_code != 200:
        raise Exception("RTSP URL not accessible")
    threading.Thread(target=start_vlc_player, daemon=True).start()
except:
    video_label = tk.Label(video_frame, text=f"Video source not available\n{RTSP_URL}", font=("Arial", 24), fg="red")
    video_label.pack(expand=True)

# Graph widget
graph_frame = tk.Frame(root, width=800, height=600, bd=0, relief="solid")
graph_frame.grid(row=0, column=1, sticky='nsew')
fig, ax = plt.subplots()
points = []
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
threading.Thread(target=update_graph, daemon=True).start()

# Gauges widget
gauges_frame = tk.Frame(root, width=400, height=400, bd=0, relief="solid")
gauges_frame.grid(row=1, column=1, sticky='nsew')
gauges = [Gauge(gauges_frame, f"Current Value {i+1}", width=200, height=150) for i in range(4)]
for i, gauge in enumerate(gauges):
    gauge.grid(row=i//2, column=i%2 , padx=50, pady=10)
threading.Thread(target=update_gauges, daemon=True).start()

# Pitch and Roll widget
pitch_roll_frame = tk.Frame(root, width=300, height=300, bd=0, relief="solid")
pitch_roll_frame.grid(row=1, column=0, sticky='nsew')
pitch_roll_canvas = PitchRoll(pitch_roll_frame, width=400, height=300)
pitch_roll_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
threading.Thread(target=update_acc_gyro, daemon=True).start()

# Status widget
status_frame = tk.Frame(root, width=400, height=100, bd=0, relief="solid")
status_frame.grid(row=2, column=0, sticky='nsew')
power_status = LedStatus(status_frame, "Power Status", width=100, height=50)
power_status.pack(side="left", padx=10)
pump_status = LedStatus(status_frame, "Pump Status", width=100, height=50)
pump_status.pack(side="left", padx=10)
misc_status = LedStatus(status_frame, "Other Status", width=100, height=50)
misc_status.pack(side="left", padx=10)
threading.Thread(target=update_status, daemon=True).start()

# Image widget
image_frame = tk.Frame(root, width=800, height=300, bd=0, relief="solid")
image_frame.grid(row=2, column=1, sticky='nsew')
image = Image.open("/home/shobhit/logo.png")
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(image_frame, image=photo)
image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Function to toggle fullscreen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Bind fullscreen toggle to F11 key
root.bind("<F11>", toggle_fullscreen)

# Main loop
root.mainloop()
