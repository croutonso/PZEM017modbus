import minimalmodbus
import serial
import time
from contextlib import closing

DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'

def read_pzem_data():
    # Initialize the connection to the PZEM device
    instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 2
    instrument.serial.timeout = 1
    
    try:
        # Read measurement data
        voltage = instrument.read_register(0x0000, number_of_decimals=2, functioncode=4)
        current = instrument.read_register(0x0001, number_of_decimals=2, functioncode=4)
        power_low = instrument.read_register(0x0002, functioncode=4)
        power_high = instrument.read_register(0x0003, functioncode=4)
        power = (power_high << 16) + power_low
        energy_low = instrument.read_register(0x0004, functioncode=4)
        energy_high = instrument.read_register(0x0005, functioncode=4)
        energy = (energy_high << 16) + energy_low
        
        # Read alarm status
        high_voltage_alarm = instrument.read_register(0x0006, functioncode=4)
        low_voltage_alarm = instrument.read_register(0x0007, functioncode=4)

        print(f"Voltage: {voltage} V")
        print(f"Current: {current} A")
        print(f"Power: {power * 0.1} W")
        print(f"Energy: {energy} Wh")
        
        # Print alarm statuses
        print(f"High Voltage Alarm: {'Alarm' if high_voltage_alarm == 0xFFFF else 'Clear'}")
        print(f"Low Voltage Alarm: {'Alarm' if low_voltage_alarm == 0xFFFF else 'Clear'}")
        
    except minimalmodbus.IllegalRequestError as e:
        print(f"Error: {e}")

    finally:
        time.sleep(1)
        instrument.serial.close()

if __name__ == "__main__":
    read_pzem_data()