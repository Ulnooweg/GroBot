# Frequently Asked Questions

## Table of Contents
[Usage Instructions](#usage-instructions)
[Terminal/SSH Login Password](#terminalssh-login-password)
[Accessing Terminal (non-SSH)](#accessing-terminal-non-ssh)

## Usage Instructions
Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details on GroBot user manual.

## Terminal/SSH Login Password
For login to the GroBot terminal, via SSH or otherwise, please consult the manual or contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca).

## Accessing Terminal (non-SSH)
There are 2 methods of accessing the terminal on the GroBot. One is via SSH which requires wifi access. Another which will be shown here is through the UART serial connection inteface. (Note: This has to be enabled on the Raspberry Pi OS. It should be enabled on the GroBot supplied by Ulnooweg Education Centre.)

### Required tools
* [USB to TTL Serial Cable](https://www.adafruit.com/product/954)
* GroBot with appropriate male header installed on the UART pins on the irrigation board.
* [PuTTY](https://www.putty.org/)

### Steps
1. Download serial cable drivers from SiLabs [CP210x Windows Drivers](https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip) and install the serial drivers.
2. Connect the serial cable to a USB port on a Windows machine.
3. Navigate to device manager and find the serial device, note down its COM port.
   - May show as "Silicon Labs CP210x USB to UART bridge (COMx)
   - note down COMx where x should be a number.
4. Connect the serial cable to the irrigation board UART header with the following cable colour configuration:
   * RED - **Do not connect**
   * BLACK --> GND
   * WHITE --> TXD
   * GREEN --> RXD
5. Now open PuTTY and connect with the following settings:
   * Mode: Serial
   * Speed: 115200
   * Serial line: COMx (COMx is the COM port found in step 3)
6. Start the connection. Press any key until a text asking for a login shows up.