from joystick_control import JoystickController

# Create instance of JoystickController
joystick = JoystickController(button_pin=19)

try:
    # Run the joystick controller
    joystick.run()

except KeyboardInterrupt:
    print("Main program interrupted. Exiting...")
