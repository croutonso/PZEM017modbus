# PZEM-004T & PZEM-017 Modbus Interface

This repository contains two Python scripts for interfacing with PZEM-004T and PZEM-017 Modbus energy monitoring devices. The scripts allow you to read the data from the devices and change their parameters.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [read_device_data.py](#read_device_datapy)
  - [set_device_parameters.py](#set_device_parameterspy)
- [FAQ](#faq)

## Requirements

- Python 3
- minimalmodbus Python library
- pySerial Python library

## Installation

1. Install Python 3 from the [official website](https://www.python.org/downloads/).

2. Install the required Python libraries by running the following command in your terminal or command prompt:

   ```
   pip install minimalmodbus pyserial
   ```

3. Clone this repository or download the Python scripts `read_device_data.py` and `set_device_parameters.py`.

## Usage

### read_device_data.py

This script reads data from the PZEM-004T or PZEM-017 device and displays the voltage, current, power, and energy values.

1. Connect the PZEM device to your computer via a USB to TTL or RS485 converter.

2. Open `read_device_data.py` in a text editor and set the `SLAVE_ADDRESS`, `DEVICE_PORT`, and other parameters according to your device and connection.

3. Save the changes and close the text editor.

4. Open a terminal or command prompt, navigate to the directory containing `read_device_data.py`, and run the following command:

   ```
   python read_device_data.py
   ```

5. The script will display the voltage, current, power, and energy values.

### set_device_parameters.py

This script allows you to change the parameters of the PZEM-004T or PZEM-017 device, such as high and low voltage alarm thresholds, slave address, and current range (PZEM-017 only).

1. Connect the PZEM device to your computer via a USB to TTL or RS485 converter.

2. Open `set_device_parameters.py` in a text editor and set the `SLAVE_ADDRESS`, `DEVICE_PORT`, and other parameters according to your device and connection.

3. Save the changes and close the text editor.

4. Open a terminal or command prompt, navigate to the directory containing `set_device_parameters.py`, and run the following command:

   ```
   python set_device_parameters.py
   ```

5. The script will display a menu with options to change various device parameters.

## FAQ

**Q: Does the slave address matter?**

A: The slave address is important to avoid conflicts between multiple Modbus devices connected to the same computer. Each device should have a unique slave address to prevent clashes and ensure proper communication.

**Q: What should I do if I already have another Modbus device connected to my computer?**

A: Make sure that each Modbus device has a unique slave address. You can change the slave address of the PZEM devices using the `set_device_parameters.py` script. Follow the steps in the [Usage](#usage) section to run the script and change the slave address.

**Q: What if the script does not work or shows an error message?**

A: Check the following:

- Ensure that the PZEM device is properly connected to your computer.
- Verify that the `SLAVE_ADDRESS`, `DEVICE_PORT`, and other parameters in the script are correctly set according to your device and connection.
- Confirm that you have installed the required Python libraries (`minimalmodbus` and `pySerial`).