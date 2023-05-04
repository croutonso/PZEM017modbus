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
        high_voltage_alarm = instrument.read_register(0x0000, functioncode=3) / 100.0
        low_voltage_alarm = instrument.read_register(0x0001, functioncode=3) / 100.0
        slave_address = instrument.read_register(0x0002, functioncode=3)
        current_range = instrument.read_register(0x0003, functioncode=3)
        return high_voltage_alarm, low_voltage_alarm, slave_address, current_range

def display_menu(current_values):
    print("\nSelect the parameter to change:")
    print("1. Set High Voltage Alarm Threshold (Current: {:.2f} V, Default: 300 V)".format(current_values[0]))
    print("2. Set Low Voltage Alarm Threshold (Current: {:.2f} V, Default: 7 V)".format(current_values[1]))
    print("3. Set Slave Address (Current: {}, Default: 1)".format(current_values[2]))
    print("4. Set Current Range (Current: {}, Default: 0)".format(CURRENT_RANGE_MAPPING[current_values[3]]))
    print("5. Reset Energy")
    print("6. Exit")

def set_high_voltage_alarm_threshold(instrument):
    value = int(input("Enter the new High Voltage Alarm Threshold (5-350 V): "))
    with closing(instrument.serial):
        instrument.write_register(0x0000, value * 100, functioncode=6)
    print("High Voltage Alarm Threshold successfully updated.")

def set_low_voltage_alarm_threshold(instrument):
    value = int(input("Enter the new Low Voltage Alarm Threshold (1-350 V): "))
    with closing(instrument.serial):
        instrument.write_register(0x0001, value * 100, functioncode=6)
    print("Low Voltage Alarm Threshold successfully updated.")

def set_slave_address(instrument):
    value = int(input("Enter the new Slave Address (1-247): "))
    with closing(instrument.serial):
        instrument.write_register(0x0002, value, functioncode=6)
    print("Slave Address successfully updated.")
    return value

def set_current_range(instrument):
    print("Enter the new Current Range:")
    print("0. 100 A")
    print("1. 50 A")
    print("2. 200 A")
    print("3. 300 A")

    value = int(input("Enter your choice: "))

    if value in [0, 1, 2, 3]:
        with closing(instrument.serial):
            instrument.write_register(0x0003, value, functioncode=6)
        print("Current Range successfully updated.")
    else:
        print("Invalid choice. Returning to the main menu.")

def reset_energy(instrument):
    instrument._perform_command(0x42, '')
    print("Energy successfully reset.")

CURRENT_RANGE_MAPPING = {
    0: "100 A",
    1: "50 A",
    2: "200 A",
    3: "300 A",
}

def main():
    instrument = connect_modbus_device(DEVICE_PORT, DEVICE_BAUDRATE, DEVICE_PARITY, DEVICE_STOPBITS)
    while True:
        try:
            current_values = read_current_values(instrument)
            display_menu(current_values)
            choice = int(input("Enter your choice: "))
            if choice == 1:
                set_high_voltage_alarm_threshold(instrument)
            elif choice == 2:
                set_low_voltage_alarm_threshold(instrument)
            elif choice == 3:
                new_address = set_slave_address(instrument)
                instrument.address = new_address
            elif choice == 4:
                set_current_range(instrument)
            elif choice == 5:
                reset_energy(instrument)
            elif choice == 6:
                break
            else:
                print("Invalid choice.")
        except minimalmodbus.NoResponseError:
            print("No response from the device. Please check the connection and try again.")
        except minimalmodbus.InvalidResponseError as e:
            print("Invalid response from the device: {}".format(str(e)))
        except Exception as e:
            print("An unexpected error occurred: {}".format(str(e)))

if __name__ == "__main__":
    main()