# Soil Moisture Testing
This directory holds in-development procedures on soil moisture testing for the Grobot.

# seesawwithmuxer.py
The PCA9548 i2c multiplexer supports up to 8 individual sensors with the same address. This allows for simultaneous data collects of the same quality in multiple locations. The example code provided is setup for two seesaw capacitive moistures sensors on channel(s) 0 and 7 to demonstrate the multiplexers range.

# PCA9548i2cdetection.py
A simple detection protocol that returns the address found at each channel of the multiplexer. Useful if the address of a sensor/component is unknown. 