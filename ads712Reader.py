import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class ACS712Reader:
    def __init__(self, adc_address=0x48, adc_gain=1):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c, address=adc_address, gain=adc_gain)
        
        # ACS712 sensitivity parameters (adjust according to your sensor model)
        self.ACS_SENSITIVITY = 0.066  # Sensitivity in mV/A (66mV per 1A for ACS712-30A)
        
        # Define AnalogIn objects for each ACS712 sensor
        self.chan_0 = AnalogIn(self.ads, ADS.P0)  # A0
        self.chan_1 = AnalogIn(self.ads, ADS.P1)  # A1
        self.chan_2 = AnalogIn(self.ads, ADS.P2)  # A2
        self.chan_3 = AnalogIn(self.ads, ADS.P3)  # A3

    def read_currents(self):
        try:
            while True:
                # Read raw ADC values
                raw_value_0 = self.chan_0.value
                raw_value_1 = self.chan_1.value
                raw_value_2 = self.chan_2.value
                raw_value_3 = self.chan_3.value
                
                # Convert raw ADC values to voltages
                voltage_0 = self.chan_0.voltage
                voltage_1 = self.chan_1.voltage
                voltage_2 = self.chan_2.voltage
                voltage_3 = self.chan_3.voltage
                
                # Convert voltages to currents
                current_0 = voltage_0 / self.ACS_SENSITIVITY
                current_1 = voltage_1 / self.ACS_SENSITIVITY
                current_2 = voltage_2 / self.ACS_SENSITIVITY
                current_3 = voltage_3 / self.ACS_SENSITIVITY
                
                print(f"Sensor 0 - Raw: {raw_value_0}, Voltage: {voltage_0:.2f}V, Current: {current_0:.2f}A")
                print(f"Sensor 1 - Raw: {raw_value_1}, Voltage: {voltage_1:.2f}V, Current: {current_1:.2f}A")
                print(f"Sensor 2 - Raw: {raw_value_2}, Voltage: {voltage_2:.2f}V, Current: {current_2:.2f}A")
                print(f"Sensor 3 - Raw: {raw_value_3}, Voltage: {voltage_3:.2f}V, Current: {current_3:.2f}A")
                
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting...")

    def close(self):
        self.ads.stop_adc()

# Example usage
if __name__ == '__main__':
    acs_reader = ACS712Reader()
    try:
        acs_reader.read_currents()
    except KeyboardInterrupt:
        acs_reader.close()
        print("\nMain program interrupted. Exiting...")
