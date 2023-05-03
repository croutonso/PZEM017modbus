import minimalmodbus
import serial

DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'

def read_pzem_data():
    instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
    instrument.serial.baudrate = BAUD_RATE
    instrument.serial.timeout = TIMEOUT
    instrument.mode = minimalmodbus.MODE_RTU

    # Read the data from the PZEM registers
    try:
        voltage = instrument.read_register(0x0000, numberOfDecimals=2)
        current = instrument.read_register(0x0001, numberOfDecimals=2)
        power_low = instrument.read_register(0x0002)
        power_high = instrument.read_register(0x0003)
        power = (power_high << 16) + power_low
        energy_low = instrument.read_register(0x0004)
        energy_high = instrument.read_register(0x0005)
        energy = (energy_high << 16) + energy_low
        high_voltage_alarm = instrument.read_register(0x0006)
        low_voltage_alarm = instrument.read_register(0x0007)

        # Print the output
        print("Voltage: {:.2f} V".format(voltage))
        print("Current: {:.2f} A".format(current))
        print("Power: {:.1f} W".format(power * 0.1))
        print("Energy: {} Wh".format(energy))
        print("High Voltage Alarm: {}".format("Alarm" if high_voltage_alarm == 0xFFFF else "Not Alarm"))
        print("Low Voltage Alarm: {}".format("Alarm" if low_voltage_alarm == 0xFFFF else "Not Alarm"))
    
    except minimalmodbus.ModbusException as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    read_pzem_data()
