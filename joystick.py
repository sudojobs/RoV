import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Define ADC parameters
ADS_GAIN = 1  # Set the gain (adjust according to your joystick)
ADS_ADDRESS = 0x48  # Default I2C address for ADS1115

# Define joystick threshold values
THRESHOLD = 20000  # Adjust this value according to your joystick sensitivity

# Define joystick directions
DIRECTIONS = {
    (1, 0): "RIGHT",
    (-1, 0): "LEFT",
    (0, 1): "UP",
    (0, -1): "DOWN",
    (0, 0): "CENTER"
}

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADS1115 ADC
ads = ADS.ADS1115(i2c, address=ADS_ADDRESS, gain=ADS_GAIN)

# Define analog input channels
analog_x = AnalogIn(ads, ADS.P0)
analog_y = AnalogIn(ads, ADS.P1)

# Main loop
try:
    while True:
        # Read analog values from joystick axes
        x_value = analog_x.value
        y_value = analog_y.value

        # Determine joystick direction based on analog readings
        direction = (0, 0)  # Default direction is CENTER
        if x_value > THRESHOLD:
            direction = (1, 0)  # RIGHT
        elif x_value < -THRESHOLD:
            direction = (-1, 0)  # LEFT
        elif y_value > THRESHOLD:
            direction = (0, 1)  # UP
        elif y_value < -THRESHOLD:
            direction = (0, -1)  # DOWN

        # Display the detected direction
        print("Joystick Direction:", DIRECTIONS.get(direction, "UNKNOWN"))

        # Wait before reading again
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    ads.deinit()  # Clean up ADC resources

