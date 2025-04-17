# Code for PCA9548 Multiplexer board; support for multiple SEESAW moisture sensors.
# This code is intented to be executed through a linux terminal.
# The RP2040 Feather is limited by I2C port count, which hinders the amount of data that can be collected.
# Furthermore, it can only read or write (not both).
# The PCA9548 is capable of streaming data from 8 separate sensors of the same address, which is useful
# for bulk collection over a long period of time.
# The following libraries are required: adafruit-circuitpython-tca9548a, adafruit-circuitpython-seesaw

# Import libraries
import time
import board
from adafruit_seesaw.seesaw import Seesaw   # Import the library for the SEESAW capacitive moisture sensor
import adafruit_tca9548a    # Import the library for the Multiplexer board

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

tca = adafruit_tca9548a.TCA9548A(i2c_bus)   # Initalizes Muxer board as the I2C Bus
ss1 = Seesaw(tca[0], addr=0x36)             # Sets the first seesaw sensor address through the I2C Bus (The Muxer), on channel 0
ss2 = Seesaw(tca[7], addr=0x36)             # Sets the second seesaw sensor address through the I2C Bus (The Muxer), on channel 7

# After initial setup, can just use sensors as normal.
while True:
    touch1 = ss1.moisture_read()            # Detect moisture from the first sensor
    touch2 = ss2.moisture_read()            # Detect moisture from the second sensor
    print("Moisture1: " + str(touch1)+ "Moisture2: " + str(touch2)) # Print the results
    time.sleep(0.1) # Sleep for 0.1 seconds