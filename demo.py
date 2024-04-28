import tkinter as tk
from tkinter import ttk
import vlc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("GUI")
        self.geometry("1920x1080")

        # Create group boxes
        self.camera_frame = ttk.LabelFrame(self, text="Camera Feed", width=1200, height=750)
        self.camera_frame.place(x=10, y=10)

        self.system_status_frame = ttk.LabelFrame(self, text="System Status", width=800, height=250)
        self.system_status_frame.place(x=10, y=770)

        self.graph_frame = ttk.LabelFrame(self, text="Graph", width=700, height=700)
        self.graph_frame.place(x=1230, y=10)

        self.analog_meter_frame = ttk.LabelFrame(self, text="Analog Meters", width=700, height=350)
        self.analog_meter_frame.place(x=1230, y=720)

        # Add exit button
        self.exit_button = ttk.Button(self, text="Exit", command=self.quit)
        self.exit_button.place(x=1830, y=1030)

        # Create VLC player instance
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()

        # Set up VLC options
        self.options = f"rtsp://192.168.10.129:8554/unicast"
        self.media = self.instance.media_new(self.options)
        self.player.set_media(self.media)

        # Get window handle for embedding
        self.camera_frame_id = self.camera_frame.winfo_id()
        self.player.set_hwnd(self.camera_frame_id)

        # Start playing
        self.player.play()

        # Plot quadratic graph
        self.plot_graph()

    def plot_graph(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        x = range(60)
        y = [i**2 for i in x]
        ax.plot(x, y)
        ax.set_title('Quadratic Graph')
        ax.set_xlabel('Minutes')
        ax.set_ylabel('Values')

        # Embed the matplotlib graph into Tkinter window
        self.graph_canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
