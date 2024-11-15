# Systems information
This file list the technical information and specifications of the GroBot.

## Hardware
Please refer to [SETTING UP YOUR GROBOT](/User_Manual/SETTING%20UP%20YOUR%20GROBOT.pdf) or [USING YOUR GROBOT](/User_Manual/USING%20YOUR%20GROBOT.pdf) for some hardware specifications, especially the parts list in section 5 of `USING YOUR GROBOT.pdf`. 

For any additional inquiries, please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details on hardware specifications.

## Software

### Description
The GroBot software consists of a main function file and many modules file which contain callable functions. The main function, main.py, controls the entire GroBot (except for LCD Display and interactions which is ran by a separate lcddispfunc.py) and calls on functions located in other modules file (such as checktimebetween in timecheck.py) as needed. The codefile main.py itself is ran in a Python virtual environment by a custom systemd process called grobot which runs on boot and will auto-restart main.py if the code encountered an error or suffered a critical failure which caused it to exit. 

The main functional loop in main.py is an infinite while loop. Every time the loop ran, it goes through the steps checking current time and sensor value and execute predefined operations in another thread if the current time and/or sensor value fits the criteria for an action initialization. After that it waits until the time ticks over to the next minute and ran the loop again. So the entire loop will only runs, at most, once per minute to ensure there are no excessive checking. 

The LCD code, lcddispfunc.py, however is separated out as it is ran constantly and independently from the main loop after being called on to run by main.py. The LCD code independently calls required functions from modules file if manual override are required outside of those functions being called by the main loop. However, the main code and lcd code still interacts through the config file, grobot_cfg.ini, as the LCD code writes any configuration changes to grobot_cfg.ini which will them be read and used by main.py as the basis for the criteria of action initialization.

There is also a oneshot systemd process called grobotboot which will run BoardMOSTFETReset.py only once upon system bootup with highest priority.

### Dependencies list
The GroBot software is built in Python3 with some dependencies on application outside of Python. The software make use of several Python pre-built libraries alongside additional non-python software which has been listed below:
1. Python built-in libraries:
   1. subprocess
   2. datetime
   3. time
   4. os
   5. threading
2. Additional Python libraries:
   1. configparser
   2. pandas
3. Adafruit Blinka built-in libraries:
   1. board
   2. busio
   3. digitalio
4. Adafruit Blinka additional libraries:
   1. adafruit-circuitpython-ahtx0
   2. adafruit-circuitpython-seesaw
   3. adafruit-circuitpython-charlcd
5. Additional software:
   1. imagemagick

### Codefiles list
The GroBot software itself is separated off into multiple files, henceforth called modules, that serves different purpose and contains different callable functions that may be imported into other module or the main codefile. Each module should also contain information on how they work. The summary of each module and their functions are summarized below:
1. main.py
   - The main codefiles containing the main loop that runs the entire GroBot code and initialize all subsystems including the LCD display.
   - There are no callable functions but this code will call imported functions from other modules to do job as required based on the schedule and sensor readings. For example calling a function to turn on the light at sunrise time.
2. BoardMOSTFETReset.py
   - MOSFET gate reset file. This code runs with highest priority on boot and immediately force all MOSFET gate into False (open circuit) state to ensure they are not at random float value which could create excessive heating.
   - There are no callable function. This code is not part of the main GroBot loop and should only be called once during boot by a separate grobotboot process.
3. config.py 
   - Provides functions to read and manipulate configuration file grobot_cfg.ini.
   - Functions include read_config(), get_plant_settings(), and update_config(section, parameter, value).
4. dataout.py
   - Provides functions to output data to excel file at a predetermined external storage location.
   - Contains a callable function excelout(T,RH,SRH) which will either create a file if it doesn't exist or append current time, temperature, humidity, and soil humidity data to the excel file.
5. diopinsetup.py
   - Provides functions to setup all required digital IO pins and object.
   - Contains a callable diopinset() function that will return pins and sensors that has been set up as a tuple of objects.
6. fancontrol.py
   - Provide functions to turn enclosure fan on or off.
   - Contains callable function fanon(t) and fanoff() which turns fan on for t seconds or off.
7. lcddispfunc.py
   - Manages the LCD display interactions, including menu navigation and manual control options. 
   - Provides functions for setting LCD color, debouncing button inputs, and handling the main menu, settings menu, and manual control menu. 
   - Also manages manual overrides for growlight, enclosure fan, and irrigation system.
   - See [LCD General Specifications](#lcd-interface) for more information.
8. lighcontrol.py
   - Provide functions to turn growlight on or off.
   - Contains callable function growlighton() and growlightoff() which turns growlight on or off.
9. grobotpicam.py
   - Provide functions that take image of the grow area using Pi camera and annotate it with a timestamp.
   - Requires imagemagick to be installed to the system as an external non-python software.
   - Contains callable function picam_capture() which takes picture using pi camera and use imagemagick to annotate the picture with timestamp.
10. sensorfeed.py
    - Provide functions that reads value from sensors and return its value.
    - Contains callable function feedread() which reads sensor value and return it as tuple of objects.
11. timecheck.py
    - Provide functions that checks if current time falls between start and end time.
    - Can handle start time that crosses midnight into end time.
    - Contains cllable function checktimebetween(starttime, endtime) that returns True or False based on if current time is between starttime and endtime or not.
12. watercontrol.py
    - Provide functions that controls the irrigation system.
    - Contain functions autorain(mmrain) and stopwater() which checks if water level is sufficient, turns on the pump and water for an amount of time corresponding to input mm of rain or stop the current watering process.
For more details please navigate to each module codefile, each should have a detailed explanation of their input, output, and functions.

### Configuration
This section list the different parameters in grobot_cfg.ini and its meaning. These value can also be changed through the LCD screen interface.
1. CameraSet
   - If Pi camera is installed or not
   - If 1, it is install and the code will take picture. If 0 it is not installed and the code will skip taking pictures.
2. dryValue
   - Raw value of humidity threshold. Range from 0 - 1000 converted to 0 - 100% on display.
   - A threshold which if the read soil humidity value drops below, watering will initiate.
3. maxTemp
   - Maximum allowable enclosure temperature in degrees Celsius.
   - Temperature above this threshold will cause the enclosure fan to turns on.
4. maxHumid
   - Maximum allowable enclosure humidity in Relative Humidity (%).
   - Humidity above this threshold will cause the enclosure fan to turns on.
5. waterVol
   - Amount of water to supply the plant with each time watering is initiated. Units in mm of rain. 
6. checkTime
   - The time for when GroBot will check whether or not to initiate watering if soil humidity is below dryValue.
   - In format of hh,mm.
   - If putting numbers into config file, make sure there are no leading zeroes (e.g. 9.02 am is input as 9,2 not 09,02)
7. sunrise
   - The time for when GroBot will turns the growlight on.
   - In format of hh,mm.
   - If putting numbers into config file, make sure there are no leading zeroes (e.g. 9.02 am is input as 9,2 not 09,02)
8. sunset
   - The time for when GroBot will turns the growlight off.
   - In format of hh,mm.
   - If putting numbers into config file, make sure there are no leading zeroes (e.g. 9.02 am is input as 9,2 not 09,02)
9. fanTime
   - Length of time enclosure fan will be on for, in seconds, if Temperature or Humidity exceeds threshold.

### LCD Interface
This section lists some specification for the LCD interface.

#### General specifications
- LCD display size of 16x2 character LCD (16 character per row, 2 row)
- LCD backlight in 3 colour options red, green, and blue.
- Negative LCD (light colour on dark background) with adjustable contrast.

#### Navigation
The LCD is controlled by 5 navigation buttons:
* Up, Down - Navigation buttons or change value (context dependent)
* Left, Right - Change value
* Select - Select the current options displayed

#### LCD Backlight Colour Coding
The colour of the LCD backlight is colour coded to indicate the current GroBot status:
* Green - Normal operations
* Blue - An action is being done e.g. Watering
* Red - An error has occured.

#### Key Functions
The LCD interface is managed by several functions in the lcddispfunc.py module:
* set_lcd_color(status): Sets the LCD backlight color based on system status.
* lcd_menu_thread(): Manages the LCD menu system in a separate thread.
* main_menu(): Displays and handles interactions with the main menu.
* settings_menu(): Allows users to modify system settings.
* manual_control_menu(): Provides options for manual system control.
* update_display(): Refreshes the LCD with current information.

### Error Logging
The GroBot have error logging capabilities. Error are logged in the process log before the GroBot process will attempt to be restarted. The following lists the error codes/message that will be output to the process log file:

- Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more information.