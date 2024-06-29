import socket
import tkinter as tk
import math
import threading
from PIL import Image, ImageTk

# Define server address and port
server_address = ('', 12345)  # Use an available port number
buffer_size = 1024

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print(f"Server listening on {server_address[0]}:{server_address[1]}")

# Initialize Tkinter
root = tk.Tk()
root.title("Bristola 2 RoV Control")

# Create Frames for group boxes
graph_frame = tk.LabelFrame(root, text="Graph", padx=10, pady=10)
graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

temp_frame = tk.LabelFrame(root, text="Temperature", padx=10, pady=10)
temp_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

pitch_roll_frame = tk.LabelFrame(root, text="Pitch and Roll", padx=10, pady=10)
pitch_roll_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

logo_frame = tk.LabelFrame(root, text="Credits", padx=10, pady=10)
logo_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

# Configure grid to adjust group boxes as per full screen
root.grid_rowconfigure(0, weight=3)  # Give more weight to the first row
root.grid_rowconfigure(1, weight=1)  # Give less weight to the second row
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create GUI elements for Graph
graph_canvas = tk.Canvas(graph_frame, bg="white")
graph_canvas.pack(expand=True, fill='both')

# Create GUI elements for Temperature
temp_canvas = tk.Canvas(temp_frame, bg="white")
temp_canvas.pack(expand=True, fill='both')
temp_label = tk.Label(temp_frame, text="0 °C", font=("Helvetica", 20, "bold"), fg="red")
temp_label.pack()

# Create GUI elements for Pitch and Roll
pitch_roll_canvas = tk.Canvas(pitch_roll_frame)
pitch_roll_canvas.pack(expand=True, fill='both')

# Load and display company logo
logo_image = Image.open("company_logo.png")  # Replace with the path to your logo image
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.pack(expand=True, fill='both')

# Global variables for pitch and roll
last_pitch = 0
last_roll = 0
gyro_stable_count = 0
GYRO_STABLE_THRESHOLD = 10  # Adjust as needed

# Function to update thermometer
def update_thermometer(temp):
    temp_canvas.delete("all")
    temp_height = (temp / 50) * temp_canvas.winfo_height()  # Assuming max temperature is 50°C
    temp_canvas.create_rectangle(25, temp_canvas.winfo_height() - temp_height, 75, temp_canvas.winfo_height(), fill="red")
    temp_label.config(text=f"{temp:.2f} °C")

# Function to calculate pitch and roll
def calculate_pitch_and_roll(gx, gy, gz):
    global last_pitch, last_roll, gyro_stable_count

    pitch = math.atan2(gy, gz) * 180 / math.pi
    roll = math.atan2(-gx, math.sqrt(gy * gy + gz * gz)) * 180 / math.pi

    # Check if gyro values are stable
    if abs(gx) < 0.5 and abs(gy) < 0.5 and abs(gz) < 0.5:
        gyro_stable_count += 1
        if gyro_stable_count >= GYRO_STABLE_THRESHOLD:
            pitch = last_pitch
            roll = last_roll
    else:
        gyro_stable_count = 0

    last_pitch = pitch
    last_roll = roll

    return pitch, roll

# Function to update pitch and roll gauge
def draw_gauge(pitch, roll):
    pitch_roll_canvas.delete("all")
    
    # Draw circular gauge
    cx, cy, r = pitch_roll_canvas.winfo_width() // 2, pitch_roll_canvas.winfo_height() // 2, min(pitch_roll_canvas.winfo_width(), pitch_roll_canvas.winfo_height()) // 2 - 10
    pitch_roll_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="white", width=2)

    # Draw sky and ground as half circles
    pitch_roll_canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=0, extent=180, fill="#4682B4", outline="")  # Darker blue
    pitch_roll_canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=180, extent=180, fill="green", outline="")

    # Draw pitch line (shorter than the circle diameter)
    pitch_radians = math.radians(pitch)
    offset_y = r * math.tan(pitch_radians)
    pitch_line_length = r * 0.9  # Slightly shorter length
    pitch_roll_canvas.create_line(cx - pitch_line_length, cy - offset_y, cx + pitch_line_length, cy + offset_y, fill="white", width=2)

    # Draw roll indicator
    roll_radians = math.radians(roll)
    roll_length = 50
    roll_x = roll_length * math.sin(roll_radians)
    roll_y = roll_length * math.cos(roll_radians)

    pitch_roll_canvas.create_oval(cx - 25, cy - 25, cx + 25, cy + 25, outline="white", width=2)
    pitch_roll_canvas.create_line(cx, cy, cx + roll_x, cy - roll_y, fill="white", width=2)

    # Draw vertical lines on the left and right sides within the circle
    vert_line_length = r / 2
    line_offset = r * 0.2  # Offset from the circle boundary
    pitch_roll_canvas.create_line(cx - r + line_offset, cy - vert_line_length, cx - r + line_offset, cy + vert_line_length, fill="white", width=2)
    pitch_roll_canvas.create_line(cx + r - line_offset, cy - vert_line_length, cx + r - line_offset, cy + vert_line_length, fill="white", width=2)

    # Draw central horizontal line connecting vertical lines
    pitch_roll_canvas.create_line(cx - r + line_offset, cy, cx + r - line_offset, cy, fill="white", width=2)

    # Display pitch and roll values on the blue part with refined font
    pitch_roll_canvas.create_text(cx, cy - r * 0.35, text=f"Pitch: {pitch:.2f}°", font=("Helvetica", 14, "bold"), fill="white")
    pitch_roll_canvas.create_text(cx, cy - r * 0.2, text=f"Roll: {roll:.2f}°", font=("Helvetica", 14, "bold"), fill="white")

# Function to update quadrature graph
def update_graph(ax, ay, gx, gy, gz, rps):
    graph_canvas.delete("all")

    # Draw grid
    for i in range(0, graph_canvas.winfo_width(), 20):
        graph_canvas.create_line([(i, 0), (i, graph_canvas.winfo_height())], tag='grid_line', fill='lightgray')
    for i in range(0, graph_canvas.winfo_height(), 20):
        graph_canvas.create_line([(0, i), (graph_canvas.winfo_width(), i)], tag='grid_line', fill='lightgray')

    # Display sensor values
    graph_canvas.create_text(10, 10, text=f"Ax: {ax:.2f} g, Ay: {ay:.2f} g, Gx: {gx:.2f} °/s, Gy: {gy:.2f} °/s, Gz: {gz:.2f} °/s, RPS: {rps:.2f}", anchor='nw', font=("Helvetica", 8))

    # Draw red dot for accelerometer data centered
    center_x = graph_canvas.winfo_width() / 2
    center_y = graph_canvas.winfo_height() / 2
    ax_scaled = ax * 50
    ay_scaled = ay * 50
    graph_canvas.create_oval(center_x - 10 + ax_scaled, center_y - 10 - ay_scaled, center_x + 10 + ax_scaled, center_y + 10 - ay_scaled, fill="red")

# Function to parse the received data
def parse_data(data):
    values = {}
    try:
        items = data.split(',')
        for item in items:
            key, value = item.split(':')
            values[key.strip()] = float(value.split()[0])
    except Exception as e:
        print(f"Error parsing data: {e}")
    return values

# Variables to store sensor data
sensor_data = {
    'Temperature': 0,
    'Ax': 0,
    'Ay': 0,
    'Gx': 0,
    'Gy': 0,
    'Gz': 0,
    'RPS': 0
}

# Function to update the GUI with the latest sensor data
def update_gui():
    temp = sensor_data.get('Temperature', 0)
    ax = sensor_data.get('Ax', 0)
    ay = sensor_data.get('Ay', 0)
    gx = sensor_data.get('Gx', 0)
    gy = sensor_data.get('Gy', 0)
    gz = sensor_data.get('Gz', 0)
    rps = sensor_data.get('RPS', 0)

    pitch, roll = calculate_pitch_and_roll(gx, gy, gz)

    update_thermometer(temp)
    draw_gauge(pitch, roll)
    update_graph(ax, ay, gx, gy, gz, rps)

    # Schedule the next update
    root.after(100, update_gui)

# Function to handle client connection and data reception
def handle_client_connection(connection):
    global sensor_data
    while True:
        try:
            # Receive data from the client
            data = connection.recv(buffer_size)
            if data:
                decoded_data = data.decode()
                print(f"Received data: {decoded_data}")

                # Parse the received data
                values = parse_data(decoded_data)
                sensor_data.update(values)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

    # Clean up the connection
    connection.close()

# Function to accept incoming connections
def accept_connections():
    while True:
        try:
            # Wait for a connection
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Handle the client connection in a separate thread
            client_thread = threading.Thread(target=handle_client_connection, args=(connection,))
            client_thread.start()

        except Exception as e:
            print(f"Error accepting connection: {e}")
            break

# Start the connection acceptance in a separate thread
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Start the Tkinter main loop with GUI update
root.after(100, update_gui)
root.mainloop()

# Clean up the server socket
server_socket.close()
