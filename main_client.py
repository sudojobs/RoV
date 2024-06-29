import socket
import smbus
from gpiozero import DigitalInputDevice
from time import sleep, time

# MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
TEMP_OUT_H = 0x41  # Temperature output register address

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
    low = bus.read_byte_data(Device_Address, addr + 1)
    
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

# Define server address and port
server_address = ('192.168.1.140', 12345)  # Replace with the server's IP address and port
buffer_size = 1024

print(f"Connecting to server at {server_address[0]}:{server_address[1]}...")

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the server for up to 3 minutes
start_time = time()
connected = False

while not connected and (time() - start_time) < 180:
    try:
        # Attempt to connect to the server
        client_socket.connect(server_address)
        connected = True
    except socket.error:
        print("Connection failed, retrying...")
        sleep(5)  # Wait 5 seconds before retrying

if not connected:
    print("Could not connect to server within 3 minutes.")
else:
    print("Connected to server.")

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
           
            # Calculate RPS (you can integrate your previous RPS calculation here if needed)
            rps = 0.0  # Placeholder for RPS calculation

            # Prepare data to send
            data = f"Gx: {Gx:.2f} °/s, Gy: {Gy:.2f} °/s, Gz: {Gz:.2f} °/s, Ax: {Ax:.2f} g, Ay: {Ay:.2f} g, Az: {Az:.2f} g, Temperature: {temperature:.2f} °C, RPS: {rps:.2f} °C"
            
            # Send data
            client_socket.sendall(data.encode())

            # Optionally, receive a response from the server
            # response = client_socket.recv(buffer_size)
            # print(f"Received from server: {response.decode()}")

            sleep(0.5)  # Pause for a second before reading values again

    except KeyboardInterrupt:
        print("\nExiting...")
        pass
    finally:
        # Clean up the socket
        client_socket.close()
