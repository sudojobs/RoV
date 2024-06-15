import time
import paho.mqtt.client as mqtt

# MQTT Broker IP address
broker_ip = "192.168.1.100"  # Replace with your MQTT broker's IP

# MQTT Topics
joystick_topic = "sensor/joystick"
acs_topic = "sensor/acs712"

# MQTT Client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mpu_topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

# Start MQTT client
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883, 60)

# Subscribe to MPU6050 data from Raspberry Pi A
client.subscribe(mpu_topic)

# Example function to handle joystick data (implement as needed)
def handle_joystick_data(data):
    print(f"Joystick data received: {data}")

# Example function to handle ACS712 sensor data (implement as needed)
def handle_acs_data(data):
    print(f"ACS712 sensor data received: {data}")

# Main loop to receive MQTT messages
client.loop_forever()
