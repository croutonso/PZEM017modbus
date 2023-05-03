import minimalmodbus
import serial
import time
import sys
import pyudev

DEVICE_ADDRESS = 0x01
PORT = '/dev/ttyUSB0'
DEVICE_BAUDRATE = 9600
DEVICE_PARITY = serial.PARITY_NONE
DEVICE_STOPBITS = 2

def connect_modbus_device(port, baudrate, parity, stopbits):
    instrument = minimalmodbus.Instrument(port, DEVICE_ADDRESS)
    instrument.serial.baudrate = baudrate
    instrument.serial.parity = parity
    instrument.serial.stopbits = stopbits
    return instrument

def reset_usb_device():
    context = pyudev.Context()

    for device in context.list_devices(subsystem='tty'):
        if device.get('ID_BUS') == 'usb':
            usb_device = device.find_parent('usb', 'usb_device')
            print(f"Resetting USB device: {usb_device.get('DEVNAME')}")
            usb_device.reset()
            break

def read_pzem_data():
    MAX_RETRIES = 3
    retries = 0

    while retries < MAX_RETRIES:
        try:
            instrument = connect_modbus_device(PORT, DEVICE_BAUDRATE, DEVICE_PARITY, DEVICE_STOPBITS)

            voltage = instrument.read_register(0x0000, 2, functioncode=4)
            current = instrument.read_register(0x0001, 2, functioncode=4)
            power = instrument.read_register(0x0003, 2, functioncode=4)
            energy = instrument.read_register(0x0005, 0, functioncode=4)

            print(f"Voltage: {voltage} V")
            print(f"Current: {current} A")
            print(f"Power: {power} W")
            print(f"Energy: {energy} Wh")

            break
        except minimalmodbus.NoResponseError as e:
            print(f"Error: {e}")
            print("Attempting to reconnect...")
            retries += 1
            reset_usb_device()
        except Exception as e:
            print(f"Error: {e}")
            break
        finally:
            time.sleep(1)
            instrument.serial.close()

    if retries == MAX_RETRIES:
        print("Failed to communicate with the device after multiple attempts. Please check the connection and try again.")
        sys.exit(1)

if __name__ == "__main__":
    read_pzem_data()
