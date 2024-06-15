import time
import board
import busio
from mpu6050 import MPU6050
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Initialize MPU6050
i2c = busio.I2C(board.SCL, board.SDA)
mpu = MPU6050(i2c)

# Initialize GPIO for shaft encoder (example)
encoder_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_pin, GPIO.IN)

# MQTT Broker IP address
broker_ip = "192.168.1.100"  # Replace with your MQTT broker's IP

# MQTT Topics
mpu_topic = "sensor/mpu6050"
encoder_topic = "sensor/shaft_encoder"

# MQTT Client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(encoder_topic)

def publish_mpu_data():
    while True:
        # Read MPU6050 data
        accel_data = mpu.acceleration
        gyro_data = mpu.gyro

        # Publish MPU6050 data to MQTT
        client.publish(mpu_topic, f"Accel: {accel_data}, Gyro: {gyro_data}")

        time.sleep(1)

# Start MQTT client
client.on_connect = on_connect
client.connect(broker_ip, 1883, 60)

# Publish MPU6050 data
publish_mpu_data()
