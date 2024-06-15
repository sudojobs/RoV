import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import Button, DigitalOutputDevice

class JoystickController:
    def __init__(self, button_pin=19, forward_pin=22, reverse_pin=23):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.x_axis = AnalogIn(self.ads, ADS.P0)
        self.y_axis = AnalogIn(self.ads, ADS.P1)
        self.button = Button(button_pin)
        self.button.when_pressed = self.on_button_press

        # GPIO pins for controlling forward and reverse
        self.forward_pin = DigitalOutputDevice(forward_pin)
        self.reverse_pin = DigitalOutputDevice(reverse_pin)

        # Thresholds for determining direction
        self.CENTER_THRESHOLD = 20000
        self.UP_THRESHOLD = 10000
        self.DOWN_THRESHOLD = 25000

    def on_button_press(self):
        print("Button pressed!")
        # Add additional actions or callbacks as needed

    def read_joystick(self):
        x_value = self.x_axis.value
        y_value = self.y_axis.value
        
        # Determine Y-axis direction
        if y_value < self.UP_THRESHOLD:
            return 'UP'
        elif y_value > self.DOWN_THRESHOLD:
            return 'DOWN'
        else:
            return 'CENTER'

    def control_motors(self, direction):
        if direction == 'UP':
            self.forward_pin.on()
            self.reverse_pin.off()
            print("Moving forward")
        elif direction == 'DOWN':
            self.forward_pin.off()
            self.reverse_pin.on()
            print("Moving reverse")
        else:
            self.forward_pin.off()
            self.reverse_pin.off()
            print("Stopping")

    def run(self):
        try:
            print("Joystick Controller running. Press Ctrl+C to exit...")
            while True:
                joystick_direction = self.read_joystick()
                self.control_motors(joystick_direction)
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nExiting...")
            self.forward_pin.off()
            self.reverse_pin.off()
            self.button.close()

if __name__ == "__main__":
    # Example usage for two joystick controllers
    joystick1 = JoystickController(button_pin=19, forward_pin=22, reverse_pin=23)
    joystick2 = JoystickController(button_pin=26, forward_pin=24, reverse_pin=25)  # Example different pins
    
    try:
        # Run both joystick controllers concurrently
        joystick1.run()
        joystick2.run()

    except KeyboardInterrupt:
        print("\nMain program interrupted. Exiting...")
