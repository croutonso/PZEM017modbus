import minimalmodbus
import serial
import time

SLAVE_ADDRESS = 0x01
DEVICE_PORT = '/dev/ttyUSB0'
DEVICE_BAUDRATE = 9600
DEVICE_PARITY = serial.PARITY_NONE

def connect_modbus_device(port, baudrate, parity):
    instrument = minimalmodbus.Instrument(port, SLAVE_ADDRESS)
    instrument.serial.baudrate = baudrate
    instrument.serial.parity = parity
    return instrument

def display_menu():
    print("Select the parameter to change:")
    print("1. Set High Voltage Alarm Threshold")
    print("2. Set Low Voltage Alarm Threshold")
    print("3. Set Slave Address")
    print("4. Set Current Range (PZEM-017 only)")
    print("5. Reset Energy")
    print("6. Exit")

def set_high_voltage_alarm_threshold(instrument):
    new_threshold = int(input("Enter new High Voltage Alarm Threshold (in 0.01V): "))
    instrument.write_register(0x0000, new_threshold, functioncode=6)
    time.sleep(1)

def set_low_voltage_alarm_threshold(instrument):
    new_threshold = int(input("Enter new Low Voltage Alarm Threshold (in 0.01V): "))
    instrument.write_register(0x0001, new_threshold, functioncode=6)
    time.sleep(1)

def set_slave_address(instrument):
    new_address = int(input("Enter new Slave Address: "))
    instrument.write_register(0x0002, new_address, functioncode=6)
    time.sleep(1)
    return new_address

def set_current_range(instrument):
    print("Current Range Options:")
    print("0: 100A")
    print("1: 50A")
    print("2: 200A")
    print("3: 300A")
    new_range = int(input("Enter new Current Range: "))
    instrument.write_register(0x0003, new_range, functioncode=6)
    time.sleep(1)

def reset_energy(instrument):
    confirm = input("Are you sure you want to reset energy? (y/n): ")
    if confirm.lower() == 'y':
        instrument.write_register(0x42, 0, functioncode=6)
        time.sleep(1)
        print("Energy reset successful.")
    else:
        print("Energy reset canceled.")

def main():
    instrument = connect_modbus_device(DEVICE_PORT, DEVICE_BAUDRATE, DEVICE_PARITY)

    while True:
        display_menu()
        user_choice = int(input("Enter your choice: "))

        if user_choice == 1:
            set_high_voltage_alarm_threshold(instrument)
            print("High Voltage Alarm Threshold changed successfully.")
        elif user_choice == 2:
            set_low_voltage_alarm_threshold(instrument)
            print("Low Voltage Alarm Threshold changed successfully.")
        elif user_choice == 3:
            new_address = set_slave_address(instrument)
            if new_address != SLAVE_ADDRESS:
                print("Slave Address changed successfully.")
                instrument = connect_modbus_device(DEVICE_PORT, DEVICE_BAUDRATE, DEVICE_PARITY)
            else:
                print("Failed to change Slave Address.")
        elif user_choice == 4:
            set_current_range(instrument)
            print("Current Range changed successfully.")
        elif user_choice == 5:
            reset_energy(instrument)
        elif user_choice == 6:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
