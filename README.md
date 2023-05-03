![Picture of PZEM-017 dive from amazon](https://github.com/croutonso/PZEM017modbus/blob/main/imgs/device.jpg?raw=true)

# PZEM-017 Modbus Interface

This repository contains two Python scripts for interfacing with PZEM-017 Modbus energy monitoring devices. The scripts allow you to read the data from the devices and change their parameters.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [pzem_reading.py](#pzem_readingpy)
  - [change_settings.py](#change_settingspy)
- [FAQ](#faq)

## Requirements

- Raspberry Pi with Raspbian OS or any Linux system
- Python 3
- minimalmodbus Python library
- pySerial Python library
- PZEM-017 energy monitoring device
- USB to RS485 converter (e.g., FTDI USB-RS485 Cable)

## Installation

1. Install Python 3 from the [official website](https://www.python.org/downloads/).

2. Install the required Python libraries by running the following command in your terminal or command prompt:

   ```
   pip install minimalmodbus pyserial
   ```

3. Clone this repository or download the Python scripts `pzem_reading.py` and `change_settings.py`.

```
git clone https://github.com/croutonso/PZEM017modbus.git
```

4. Connect the PZEM device to your Raspberry Pi or Linux system using a USB to RS485 converter.

## Usage

### pzem_reading.py

This script reads data from the PZEM-017 device and displays the voltage, current, power, and energy values.

1. Open `pzem_reading.py` in a text editor and set the `DEVICE_ADDRESS`, `PORT`, and other parameters according to your device and connection.

2. Save the changes and close the text editor.

3. Open a terminal, navigate to the directory containing `pzem_reading.py`, and run the following command:

   ```
   python pzem_reading.py
   ```

4. The script will display the voltage, current, power, and energy values.

### change_settings.py

This script allows you to change the parameters of the PZEM-017 device, such as high and low voltage alarm thresholds, slave address, and current range (PZEM-017 only).

1. Open `change_settings.py` in a text editor and set the `SLAVE_ADDRESS`, `DEVICE_PORT`, and other parameters according to your device and connection.

2. Save the changes and close the text editor.

3. Open a terminal, navigate to the directory containing `change_settings.py`, and run the following command:

   ```
   python change_settings.py
   ```

4. The script will display a menu with options to change various device parameters.

## FAQ

**Q: Does the slave address matter?**

A: The slave address is important to avoid conflicts between multiple Modbus devices connected to the same computer. Each device should have a unique slave address to prevent clashes and ensure proper communication.

**Q: What should I do if I already have another Modbus device connected to my computer?**

A: Make sure that each Modbus device has a unique slave address. You can change the slave address of the PZEM devices using the `change_settings.py` script. Follow the steps in the [Usage](#usage) section to run the script and change the slave address.

**Q: What if the script does not work or shows an error message?**

A: Check the following:

- Ensure that the PZEM device is properly connected to your computer.
- Verify that the `DEVICE_ADDRESS`, `PORT`, and other parameters in the script are correctly set according to your device and connection.
- Confirm that you have installed the required Python libraries (`minimalmodbus` and `pySerial`).

**Q: Where can I find more information about the PZEM-004T and PZEM-017 devices?**

A: You can find more information about the devices on their respective product pages:

- [PZEM-017 info page](https://solarduino.com/pzem-017-dc-energy-meter-with-arduino/)

**Q: How do I identify the correct port for my device on my Raspberry Pi or Linux system?**

A: You can run the following command to list available serial ports:

```
dmesg | grep tty
```

Look for lines containing `ttyUSB` or `ttyAMA`. The port name should look like `/dev/ttyUSB0` or `/dev/ttyAMA0`. Use this port name in the `PORT` variable in the Python scripts.

**Q: Can I use these scripts on a Windows system?**

A: Yes, these scripts can be used on a Windows system. You will need to adjust the `PORT` variable in the Python scripts to the appropriate COM port for your device (e.g., `COM3`). You can check available COM ports in the Device Manager under "Ports (COM & LPT)".

**Q: How do I install the minimalmodbus and pySerial libraries on a Raspberry Pi or Linux system?**

A: You can install the libraries using the following command:

```
pip3 install minimalmodbus pyserial
```

Make sure you are using `pip3` for Python 3 installations.

**Q: How do I run the scripts with Python 3 on a Raspberry Pi or Linux system?**

A: You can run the scripts with Python 3 using the following command:

```
python3 script_name.py
```

Replace `script_name.py` with the name of the script you want to run, such as `pzem_reading.py` or `change_settings.py`.
