#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/TNarakol-UEC/GroBot
#
########################################
#
#Contact: engineering@ulnooweg.ca
#Growth Enclosure 
#
#LCD Module control code
#V1.0.3
#
########################################

import board
import time
from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C
import threading
from lightcontrol import growlighton, growlightoff
from fancontrol import fanon, fanoff
from watercontrol import autorain, stopwater
from picamera import picam_capture
import config
from timecheck import checktimebetween
from datetime import datetime, time as datetime_time
import subprocess  # Import for setting the system time
from config import get_plant_settings

# Global variables for manual override and watering state
manual_override = {
    "light": False,
    "fan": False,
    "watering": False
}

watering_active = False

i2c = board.I2C()  # uses board.SCL and board.SDA
lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

def set_lcd_color(status):
    """Set LCD color based on status."""
    if status == "normal":
        lcd.color = [0, 100, 0]  # Green
    elif status == "in_progress":
        lcd.color = [0, 0, 100]  # Blue
    elif status == "error":
        lcd.color = [100, 0, 0]  # Red

def debounce(button):
    """ Debounce a button property """
    button_state = button()  # Initial state
    last_change_time = time.monotonic()
    while True:
        current_time = time.monotonic()
        if button() != button_state:
            last_change_time = current_time
        button_state = button()
        if current_time - last_change_time > 0.1:  # Wait for stable state for 100ms
            break
    return button_state

def display_menu(options, index):
    """Helper function to display menu options with the current selection on the bottom line."""
    lcd.clear()
    lcd.message = f"Select Option:\n{options[index][:16]}"

def clear_and_return_to_menu():
    """Clear the LCD and return to the main menu."""
    apply_settings()  # Ensure the latest settings are applied
    lcd.clear()
    main_menu()

def edit_settings_menu():
    """Function to navigate and edit settings."""
    options = ['System Time', 'Sunrise Time', 'Sunset Time', 'Irrigation', 'Temp Setpoint', 'Humidity Setpoint', 'Camera Yes/No', 'Back']
    index = 0
    display_menu(options, index)
    while True:
        update = False
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            index = (index - 1) % len(options)
            update = True
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            index = (index + 1) % len(options)
            update = True
        if update:
            display_menu(options, index)
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            if options[index] == 'System Time':
                adjust_system_time('System Time')
            elif options[index] == 'Sunrise Time':
                adjust_time_parameter('sunrise', 'Sunrise Time')
            elif options[index] == 'Sunset Time':
                adjust_time_parameter('sunset', 'Sunset Time')
            elif options[index] == 'Irrigation':
                irrigation_menu()
            elif options[index] == 'Temp Setpoint':
                adjust_parameter('maxTemp', 1, 0, 50, 'Temperature Setpoint')
            elif options[index] == 'Humidity Setpoint':
                adjust_parameter('maxHumid', 5, 0, 100, 'Humidity Setpoint')
            elif options[index] == 'Camera Yes/No':
                cfg = config.read_config()
                cam_set = cfg['PICAMERA']['CameraSet']
                config.update_config('PICAMERA', 'CameraSet', '0' if cam_set == '1' else '1')
                apply_settings()  # Apply the camera setting change
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)  # Pause before returning to menu

def adjust_parameter(parameter_name, step, min_val, max_val, display_name):
    """General function to adjust a numerical parameter."""
    cfg = config.read_config()
    value = int(cfg['PLANTCFG'][parameter_name])
    lcd.clear()
    lcd.message = f"{display_name}:\n{value}"
    while True:
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            value = min(value + step, max_val)
            lcd.clear()
            lcd.message = f"{display_name}:\n{value}"
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            value = max(value - step, min_val)
            lcd.clear()
            lcd.message = f"{display_name}:\n{value}"
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            config.update_config('PLANTCFG', parameter_name, str(value))
            apply_settings()  # Apply the parameter change
            lcd.clear()
            lcd.message = f"Set to:\n{value}"
            time.sleep(1)  # Show the set message
            return
        time.sleep(0.2)  # Reduce refresh rate to minimize jitter


def adjust_time_parameter(parameter_name, display_name):
    """Function to adjust time parameters (HH:MM)."""
    cfg = config.read_config()
    value = [int(x) for x in cfg['PLANTCFG'][parameter_name].split(",")]
    hours, minutes = value
    lcd.clear()
    lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
    while True:
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            hours = (hours + 1) % 24
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            hours = (hours - 1) % 24
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.right_button:
            debounce(lambda: lcd.right_button)
            minutes = (minutes + 1) % 60
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.left_button:
            debounce(lambda: lcd.left_button)
            minutes = (minutes - 1) % 60
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            config.update_config('PLANTCFG', parameter_name, f"{hours},{minutes}")
            apply_settings()  # Apply the time parameter change
            lcd.clear()
            lcd.message = f"Set to:\n{hours:02d}:{minutes:02d}"
            time.sleep(1)  # Show the set message
            return
        time.sleep(0.2)  # Reduce refresh rate to minimize jitter

def adjust_system_time(display_name):
    """Function to adjust the system time (HH:MM) and update the RTC."""
    now = datetime.now()
    hours, minutes = now.hour, now.minute
    lcd.clear()
    lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
    while True:
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            hours = (hours + 1) % 24
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            hours = (hours - 1) % 24
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.right_button:
            debounce(lambda: lcd.right_button)
            minutes = (minutes + 1) % 60
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.left_button:
            debounce(lambda: lcd.left_button)
            minutes = (minutes - 1) % 60
            lcd.clear()
            lcd.message = f"{display_name}:\n{hours:02d}:{minutes:02d}"
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            new_time = f"{hours:02d}:{minutes:02d}:00"
            try:
                # Set the system time
                subprocess.run(["sudo", "date", f"--set={new_time}"], check=True)
                
                # Update the RTC with the new system time
                subprocess.run(["sudo", "hwclock", "-w"], check=True)
                
                apply_settings()  # Apply the system time change
                lcd.clear()
                lcd.message = f"Time Set to:\n{new_time}"
            except Exception as e:
                lcd.clear()
                lcd.message = f"Error:\n{str(e)}"
            time.sleep(1)  # Show the set message
            return
        time.sleep(0.2)  # Reduce refresh rate to minimize jitter
        
def irrigation_menu():
    """Function to navigate and edit irrigation settings."""
    options = ['Soil Moist Thresh', 'Water Vol', 'Watering Time', 'Back']
    index = 0
    display_menu(options, index)
    while True:
        update = False
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            index = (index - 1) % len(options)
            update = True
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            index = (index + 1) % len(options)
            update = True
        if update:
            display_menu(options, index)
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            if options[index] == 'Soil Moist Thresh':
                adjust_soil_moisture_threshold()
            elif options[index] == 'Water Vol':
                adjust_parameter('waterVol', 1, 0, 50, 'Water mm of Rain')
            elif options[index] == 'Watering Time':
                adjust_time_parameter('checkTime', 'Watering Time')
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)  # Pause before returning to menu
def adjust_soil_moisture_threshold():
    """Function to adjust soil moisture threshold as a percentage."""
    cfg = config.read_config()
    value = int(cfg['PLANTCFG']['dryValue'])
    percentage = int((value / 1000) * 100)  # Convert to percentage
    lcd.clear()
    message = f"Soil Moisture %:\n{percentage}%"
    lcd.message = message
    last_update = time.monotonic()
    hold_start = None
    while True:
        current_time = time.monotonic()
        if lcd.up_button:
            if hold_start is None:
                hold_start = current_time
                percentage = min(percentage + 1, 100)
            elif current_time - hold_start > 0.5:  # Hold for 0.5 seconds
                percentage = min(percentage + 10, 100)
            if current_time - last_update > 0.1:  # Update display every 0.1 seconds
                message = f"Soil Moisture %:\n{percentage}%"
                lcd.message = message
                last_update = current_time
        elif lcd.down_button:
            if hold_start is None:
                hold_start = current_time
                percentage = max(percentage - 1, 0)
            elif current_time - hold_start > 0.5:  # Hold for 0.5 seconds
                percentage = max(percentage - 10, 0)
            if current_time - last_update > 0.1:  # Update display every 0.1 seconds
                message = f"Soil Moisture %:\n{percentage}%"
                lcd.message = message
                last_update = current_time
        else:
            hold_start = None
        if lcd.select_button:
            debounce(lambda: lcd.select_button)
            value = int((percentage / 100) * 1000)  # Convert back to 0-1000 range
            config.update_config('PLANTCFG', 'dryValue', str(value))
            apply_settings()  # Apply the parameter change
            lcd.clear()
            message = f"Set to:\n{percentage}%"
            lcd.message = message
            time.sleep(1)  # Show the set message
            clear_and_return_to_menu()
            break
        time.sleep(0.05)  # Reduce CPU usage

def manual_control_menu():
    """Function to handle manual controls."""
    options = ['Take Picture Now', 'Water Now', 'Stop Watering Now', 'Light On Now', 'Light Off Now', 'Fan On Now', 'Fan Off Now', 'Back']
    index = 0
    display_menu(options, index)
    while True:
        update = False
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            index = (index - 1) % len(options)
            update = True
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            index = (index + 1) % len(options)
            update = True
        if update:
            display_menu(options, index)
        elif lcd.select_button:
            # Wait for button release to avoid multiple triggers
            while lcd.select_button:
                time.sleep(0.01)
            if options[index] == 'Take Picture Now':
                start_picture_thread()
            elif options[index] == 'Water Now':
                start_watering_thread()
            elif options[index] == 'Stop Watering Now':
                control_watering(False)
            elif options[index] == 'Light On Now':
                control_light(True)
            elif options[index] == 'Light Off Now':
                control_light(False)
            elif options[index] == 'Fan On Now':
                start_fan_thread()
            elif options[index] == 'Fan Off Now':
                control_fan(False)
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)  # Pause before returning to menu
        time.sleep(0.05)  # Small delay to reduce CPU usage

def start_fan_thread():
    """Start the fan in a separate thread."""
    threading.Thread(target=control_fan, args=(True,)).start()

def start_picture_thread():
    """Start the picture-taking process in a separate thread."""
    threading.Thread(target=control_picture).start()

def start_watering_thread():
    """Start a thread for the watering process."""
    global watering_active
    watering_active = True
    threading.Thread(target=control_watering, args=(True,)).start()

def control_light(turn_on):
    """Control the grow light."""
    global manual_override
    try:
        if turn_on:
            print("Turning on the light...")  # Debugging line
            result = growlighton()
            manual_override["light"] = True
            lcd.clear()
            lcd.message = "Light On" if result else "Light On Failed"
        else:
            print("Turning off the light...")  # Debugging line
            result = growlightoff()
            manual_override["light"] = False
            lcd.clear()
            lcd.message = "Light Off" if result else "Light Off Failed"
        print(f"Light control result: {result}")  # Debugging line
        time.sleep(2)  # Keep the message for 2 seconds
    except Exception as e:
        print(f"Error in control_light: {e}")  # Debugging line
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)

def control_picture():
    """Control the picture-taking process."""
    try:
        result = picam_capture()
        lcd.clear()
        lcd.message = "Picture Taken" if result else "Picture Failed"
        time.sleep(2)  # Keep the message for 2 seconds
    except Exception as e:
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)

def control_watering(start):
    """Control the watering system."""
    global manual_override, watering_active
    try:
        settings = config.get_plant_settings()  # Get the latest settings
        if start:
            print("Starting watering...")  # Debugging line
            result = autorain(settings['waterVol'])
            manual_override["watering"] = True
            lcd.clear()
            lcd.message = "Watering" if result == 1 else "Watering Failed"
            if result == 2:
                lcd.message = "Low Water"
            print(f"Watering control result: {result}")  # Debugging line
        else:
            print("Stopping watering...")  # Debugging line
            result = stopwater()
            manual_override["watering"] = False
            watering_active = False
            lcd.clear()
            lcd.message = "Water Stopped" if result else "Stop Failed"
            print(f"Water stopping result: {result}")  # Debugging line
        time.sleep(2)  # Keep the message for 2 seconds
    except Exception as e:
        print(f"Error in control_watering: {e}")  # Debugging line
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)

def return_to_initial_screen():
    """Function to display the initial LCD screen with time and prompt."""
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        lcd.message = f"{current_time}\nPress Select"
        if lcd.select_button:
            debounce(lambda: lcd.select_button)
            main_menu()  # Return to the main menu when "Select" is pressed
            break  # Exit the loop when "Select" is pressed
        time.sleep(1)  # Refresh the time every second

def control_fan(turn_on):
    """Control the fan."""
    global manual_override
    try:
        settings = config.get_plant_settings()  # Get the latest settings
        if turn_on:
            print("Turning on the fan...")  # Debugging line
            result = fanon(settings['fanTime'])
            manual_override["fan"] = True
            lcd.clear()
            lcd.message = "Fan On" if result else "Fan On Failed"
            print(f"Fan control result: {result}")  # Debugging line
        else:
            print("Turning off the fan...")  # Debugging line
            result = fanoff()
            manual_override["fan"] = False
            lcd.clear()
            lcd.message = "Fan Off" if result else "Fan Off Failed"
            print(f"Fan stopping result: {result}")  # Debugging line
        time.sleep(2)  # Keep the message for 2 seconds
    except Exception as e:
        print(f"Error in control_fan: {e}")  # Debugging line
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)

def apply_settings(): # Important note, not required to check every settings let main loop run
    
    # global settings
    # settings = get_plant_settings()  # Re-read the latest settings from the config file

    # Immediately apply the settings that require real-time updates
    # if checktimebetween(datetime_time(settings['sunrise'][0], settings['sunrise'][1]), datetime_time(settings['sunset'][0], settings['sunset'][1])):
    #     growlighton()
    # else:
    #     growlightoff()

    # if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
    #     fanon(settings['fanTime'])
    # else:
    #     fanoff()

    return



# Add a function to convert the mm to pump second.  


def main_menu():
    """Function to navigate between different settings."""
    options = ['Edit Settings', 'Manual Control', 'Back']
    index = 0
    display_menu(options, index)
    while True:
        update = False
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            index = (index - 1) % len(options)
            update = True
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            index = (index + 1) % len(options)
            update = True
        if update:
            display_menu(options, index)
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            if options[index] == 'Edit Settings':
                edit_settings_menu()
            elif options[index] == 'Manual Control':
                manual_control_menu()
            elif options[index] == 'Back':
                return  # Return to the previous level
            display_menu(options, index)
            time.sleep(0.5)  # Pause before returning to menu

def lcd_menu_thread():
    lcd.clear()
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        lcd.message = f"{current_time}\nPress Select"
        if lcd.select_button:
            debounce(lambda: lcd.select_button)
            main_menu()
            lcd.clear()
        time.sleep(1)  # Refresh the time every second
