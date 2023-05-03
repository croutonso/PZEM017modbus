# PZEM-017
# PZEM Reader

This Python script reads data from the PZEM-003/017 DC communication module using the Modbus-RTU protocol. The script prints the output with the appropriate title and units, including error codes.

## Dependencies

This script requires the minimalmodbus library. Install it using:

```
pip install minimalmodbus
```

## Usage

Before running the script, make sure to set the appropriate serial port in the PORT variable.

Run the script using:

```
python pzem_reader.py
```

## Notes

- This script only supports reading data from the PZEM module and does not include functionality for setting any parameters or running calibrations.
- The PZEM-003/017 module should be connected to the PC using a USB-to-RS485 converter.
- Do not use the USB port provided by your PC as an independent power supply for the PZEM module, as it may damage your PC.
```