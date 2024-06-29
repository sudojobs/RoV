import smbus
from gpiozero import DigitalInputDevice
from time import sleep
from time import time 
from gpiozero import DigitalInputDevice


# MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
TEMP_OUT_H   = 0x41  # Temperature output register address

def calculate_rps(sample_time=1, steps_per_revolution=20):
    """
    Calculate Revolutions Per Second (RPS)

    :param sample_time: Sampling time in seconds
    :param steps_per_revolution: Number of steps in each complete revolution
    :return: Revolutions per second
    """
    start_time = time()
    end_time = start_time + sample_time
    steps = 0
    last_state = False

    while time() < end_time:
        current_state = sensor.is_active
        if current_state and not last_state:
            # Detect a transition from inactive to active state
            steps += 1
        last_state = current_state

    # Calculate RPS
    rps = steps / steps_per_revolution
    return rps

# Initialize MPU6050
def MPU_Init():
    # Write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# Read temperature from MPU6050
def read_temperature():
    raw_temperature = read_raw_data(TEMP_OUT_H)
    actual_temperature = (raw_temperature / 340.0) + 36.53  # See MPU6050 datasheet for conversion formula
    return actual_temperature

# Read raw data from MPU6050
def read_raw_data(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    # Concatenate higher and lower value
    value = ((high << 8) | low)
    
    # To get signed value from MPU6050
    if value > 32768:
        value = value - 65536
    return value

# Initialize MPU6050
bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address
MPU_Init()

sensor = DigitalInputDevice(17)  # Assuming the sensor is connected to GPIO17

print("Reading Data from MPU6050, GPIO 17, and Temperature... Press Ctrl+C to exit")

try:
    while True:
        # Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        # Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x / 16384.0
        Ay = acc_y / 16384.0
        Az = acc_z / 16384.0
        
        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0
        
        # Read temperature
        temperature = read_temperature() 
       

        #read encoder data rps
           
        rps=calculate_rps();
    
        # Print all data
        print(f"Gx: {Gx:.2f} °/s\tGy: {Gy:.2f} °/s\tGz: {Gz:.2f} °/s\tAx: {Ax:.2f} g\tAy: {Ay:.2f} g\tAz: {Az:.2f} g\tTemperature: {temperature:.2f} °C\tRPS: {rps:.2f} °C")
        sleep(0.5)  # Pause for a second before reading values again

except KeyboardInterrupt:
    # Safely exit the program when a keyboard interrupt is detected
    print("\nExiting...")
    pass
