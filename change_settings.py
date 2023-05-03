import minimalmodbus
import serial
import time
from contextlib import closing

SLAVE_ADDRESS = 0x01
DEVICE_PORT = '/dev/ttyUSB0'
DEVICE_BAUDRATE = 9600
DEVICE_PARITY = serial.PARITY_NONE
DEVICE_STOPBITS = 2

def connect_modbus_device(port, baudrate, parity, stopbits):
    instrument = minimalmodbus.Instrument(port, SLAVE_ADDRESS)
    instrument.serial.baudrate = baudrate
    instrument.serial.bytesize = 8
    instrument.serial.parity = parity
    instrument.serial.stopbits = stopbits
    instrument.serial.timeout = 1
    return instrument

def read_current_values(instrument):
    with closing(instrument.serial):
        time.sleep(1)
        high_voltage_alarm = instrument.read_register(0x0000, functioncode=4)
        low_voltage_alarm = instrument.read_register(0x0001, functioncode=4)
        slave_address = instrument.read_register(0x0002, functioncode=4)
        current_range = instrument.read_register(0x0003, functioncode=4)
        return high_voltage_alarm, low_voltage_alarm, slave_address, current_range

def display_menu(current_values):
    print("\nSelect the parameter to change:")
    print("1. Set High Voltage Alarm Threshold (Current: {} V, Default: 250 V)".format(current_values[0]))
    print("2. Set Low Voltage Alarm Threshold (Current: {} V, Default: 0 V)".format(current_values[1]))
    print("3. Set Slave Address (Current: {}, Default: 1)".format(current_values[2]))
    print("4. Set Current Range (PZEM-017 only) (Current: {}, Default: 0)".format(current_values[3]))
    print("5. Reset Energy")
    print("6. Exit")

def set_high_voltage_alarm_threshold(instrument):
    value = int(input("Enter the new High Voltage Alarm Threshold (0-300 V): "))
    with closing(instrument.serial):
        instrument.write_register(0x0000, value, functioncode=6)

def set_low_voltage_alarm_threshold(instrument):
    value = int(input("Enter the new Low Voltage Alarm Threshold (0-300 V): "))
    with closing(instrument.serial):
        instrument.write_register(0x0001, value, functioncode=6)

def set_slave_address(instrument):
    value = int(input("Enter the new Slave Address (1-247): "))
    with closing(instrument.serial):
        instrument.write_register(0x0002, value, functioncode=6)
    return value

def set_current_range(instrument):
    value = int(input("Enter the new Current Range (0 for 5 A, 1 for 100 A): "))
    with closing(instrument.serial):
        instrument.write_register(0x0003, value, functioncode=6)

def reset_energy(instrument):
    with closing(instrument.serial):
        instrument.write_register(0x0005, 0, functioncode=6)

def main():
    instrument = connect_modbus_device(DEVICE_PORT, DEVICE_BAUDRATE, DEVICE_PARITY, DEVICE_STOPBITS)
    
    while True:
        current_values = read_current_values(instrument)
        display_menu(current_values)
        user_choice = int(input("Enter your choice: "))
        
        try:
            if user_choice == 1:
                set_high_voltage_alarm_threshold(instrument)
                print("High Voltage Alarm Threshold changed successfully.")
                instrument.serial.close()
            elif user_choice == 2:
                set_low_voltage_alarm_threshold(instrument)
                print("Low Voltage Alarm Threshold changed successfully.")
                instrument.serial.close()
            elif user_choice == 3:
                new_address = set_slave_address(instrument)
                instrument.serial.close()
                if new_address != SLAVE_ADDRESS:
                    print("Slave Address changed successfully.")
                    instrument = connect_modbus_device(DEVICE_PORT, DEVICE_BAUDRATE, DEVICE_PARITY, DEVICE_STOPBITS)
                else:
                    print("Failed to change Slave Address.")
            elif user_choice == 4:
                set_current_range(instrument)
                print("Current Range changed successfully.")
                instrument.serial.close()
            elif user_choice == 5:
                reset_energy(instrument)
                instrument.serial.close()
            elif user_choice == 6:
                break
            else:
                print("Invalid choice. Please try again.")
                instrument.serial.close()
        except minimalmodbus.NoResponseError as e:
            print(f"Error: {e}")
            print("Please make sure the device is connected and the correct port is specified.")
            break
        
        except Exception as e:
            print(f"Error: {e}")
            break
        
    if instrument.serial.is_open:
        instrument.serial.close()
        
if __name__ == "__main__":
    main()
    