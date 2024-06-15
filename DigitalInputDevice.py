from gpiozero import DigitalInputDevice
import time

def read_gpio_status(pin):
    # Create a DigitalInputDevice object for the specified GPIO pin
    gpio_input = DigitalInputDevice(pin)

    try:
        while True:
            # Read the current state of the GPIO pin (True for On/High, False for Off/Low)
            status = gpio_input.value

            if status:
                print(f"GPIO pin {pin} is ON")
            else:
                print(f"GPIO pin {pin} is OFF")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting...")
        gpio_input.close()

# Example usage
if __name__ == '__main__':
    # Replace `17` with your GPIO pin number
    read_gpio_status(17)
