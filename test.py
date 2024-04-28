import tkinter as tk
from tkinter import ttk
#from PIL import Image, ImageTk
import vlc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("GUI")
        self.geometry("1920x1080")

        # Remove window frame
        self.overrideredirect(True)

        # Create group boxes
        self.camera_frame = ttk.LabelFrame(self, text="Camera Feed", width=800, height=600)
        self.camera_frame.place(x=10, y=10)

        self.system_status_frame = ttk.LabelFrame(self, text="System Status", width=500, height=200)
        self.system_status_frame.place(x=10, y=620)
        
        self.system_status_frame = ttk.LabelFrame(self, text="RoV Pitch and Rolls", width=290, height=300)
        self.system_status_frame.place(x=520, y=620)

        self.graph_frame = ttk.LabelFrame(self, text="Graph", width=700, height=400)
        self.graph_frame.place(x=820, y=10)

        self.analog_meter_frame = ttk.LabelFrame(self, text="Analog Meters", width=700, height=400)
        self.analog_meter_frame.place(x=820, y=420)

        # Create analog meters
        for i in range(2):
            analog_meter = ttk.Progressbar(self.analog_meter_frame, orient="horizontal", length=200, mode="determinate")
            analog_meter.grid(row=0, column=i, padx=10, pady=10)
            analog_meter["value"] = 50  # Set default value
                # Add exit button
                
        self.exit_button = ttk.Button(self, text="Exit", command=self.quit)
        self.exit_button.place(x=1400, y=900)
        
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


        # Load logo image
        #self.logo_image = Image.open("logo.png")
        #self.logo_image = self.logo_image.resize((200, 200), Image.ANTIALIAS)
        #self.logo_image = ImageTk.PhotoImage(self.logo_image)

        # Add logo to the GUI
        #self.logo_label = tk.Label(self, image=self.logo_image)
        #self.logo_label.place(x=10, y=880)    
        
        # Plot quadratic graph
        self.plot_graph()

        # Add system status LEDs
        self.add_led(self.system_status_frame, "System Power", 50, 30, "red")
        self.add_led(self.system_status_frame, "Pump On", 50, 90, "green")
        self.add_led(self.system_status_frame, "RoV Communication", 50, 150, "green")


    def add_led(self, parent, label_text, x, y, color):
        # Create canvas for LED
        canvas = tk.Canvas(parent, width=30, height=30)
        canvas.create_oval(5, 5, 25, 25, fill=color, outline="black")
        canvas.place(x=x, y=y)

        # Add label
        label = ttk.Label(parent, text=label_text)
        label.place(x=x + 40, y=y + 5)
        
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
    exit_button = Button(app, text="Exit", command=app.destroy) 
    exit_button.pack(pady=20)