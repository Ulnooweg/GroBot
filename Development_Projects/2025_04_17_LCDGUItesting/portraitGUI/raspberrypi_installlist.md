[Config]
### Display Drivers
dtoverlay=vc4-kms-dsi-waveshare-panel,2_8_inch

[.config/wf-panel-pi.ini]
### Hide Taskbar
autohide=true
autohide_duration=500

[Pip3]
### Datetime
datetime
### GUI
pyside6
### Adafruit Moisture Sensing
Adafruit_CircuitPython_TCA9548A
adafruit-circuitpython-seesaw

[Other]
sudo apt-get install -y libxcb-cursor-dev
### Adafruit Drivers
Blinka (see working document)
### Adjustable Brightness
wget https://files.waveshare.com/upload/f/f4/Brightness.zip
unzip Brightness.zip
cd Brightness
sudo chmod +x install.sh
./install.sh