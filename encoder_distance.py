import gpiod
import time
import math

# GPIO pin connected to the encoder (BCM numbering)
ENCODER_PIN = 17
CHIP = 'gpiochip0'  # The GPIO chip to use

# Initialize variables
rotation_count = 0

# Wheel parameters
wheel_diameter = 0.1  # in meters (example: 10 cm)
pulses_per_revolution = 20  # example value, change as per your encoder specification

# Calculate the wheel circumference and distance per pulse
wheel_circumference = math.pi * wheel_diameter
distance_per_pulse = wheel_circumference / pulses_per_revolution

# Define the callback function for the encoder
def encoder_callback(event):
    global rotation_count
    if event.type == gpiod.LineEvent.RISING_EDGE:
        rotation_count += 1
        total_distance = rotation_count * distance_per_pulse
        print(f"Rotation count: {rotation_count}, Distance traveled: {total_distance:.4f} meters")

# Setup gpiod
chip = gpiod.Chip(CHIP)
line = chip.get_line(ENCODER_PIN)
line.request(consumer="encoder", type=gpiod.LINE_REQ_EV_RISING_EDGE)

print("Counting wheel rotations and calculating distance. Press Ctrl+C to stop.")

try:
    while True:
        event = line.event_wait(sec=1)
        if event:
            event = line.event_read()
            encoder_callback(event)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    line.release()
    chip.close()
