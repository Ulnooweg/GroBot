#Copyright 2023-2024 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: lcddispfunc
#Version: 1.1
#Description: LCD Module control code
#Function: Controls the workings of the LCD display and human interaction. Consult Info.md for more information
#Input: consult Info.md
#Output: consult Info.md
#Error Handling: consult Info.md
#
########################################
### Git check  



import board
import time
from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C
import threading
from lightcontrol import growlighton, growlightoff
from fancontrol import fanon, fanoff
from watercontrol import autorain, stopwater
from grobotpicam import picam_capture
import config
from timecheck import checktimebetween
from datetime import datetime, time as datetime_time
import subprocess  # Import for setting the system time
from config import (
    get_plant_settings, 
    get_version_info,
    readcsv,
    readcsv_softver
)import updatefw
from logoutput import logtofile
from diopinsetup import diopinset

diop = diopinset()
s1, s2, s3, s4, s5, s6, b1, ths, sms = diop[0], diop[1], diop[2], diop[3], diop[4], diop[5], diop[6], diop[7], diop[8]

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
        lcd.rgb = [0, 100, 0]    # Ensure RGB values are set properly
    elif status == "in_progress":
        lcd.color = [0, 0, 100]  # Blue
        lcd.rgb = [0, 0, 100]    # Set RGB explicitly
        # Adjust contrast for better visibility on blue background
        lcd.contrast = 60        # Adjust this value (0-255) for best visibility
    elif status == "error":
        lcd.color = [100, 0, 0]  # Red
        lcd.rgb = [100, 0, 0]    # Set RGB explicitly
    
    # Reset contrast when not blue
    if status != "in_progress":
        lcd.contrast = 40        # Default contrast value

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
    option_text = options[index]
    if len(option_text) > 16:  # If text is longer than LCD width
        # Show first 13 chars + "..." to indicate more
        lcd.message = f"Select Option:\n{option_text[:13]}..."
        time.sleep(1)  # Wait a second
        # Then scroll the full text
        start_pos = 0
        while start_pos + 16 <= len(option_text):
            lcd.clear()
            lcd.message = f"Select Option:\n{option_text[start_pos:start_pos+16]}"
            start_pos += 1
            time.sleep(0.3)  # Adjust speed as needed
        # Return to beginning
        lcd.clear()
        lcd.message = f"Select Option:\n{option_text[:16]}"
    else:
        lcd.message = f"Select Option:\n{option_text[:16]}"

def clear_and_return_to_menu():
    """Clear the LCD and return to the main menu."""
    apply_settings()  # Ensure the latest settings are applied
    lcd.clear()
    main_menu()

def edit_settings_menu():
    """Function to navigate and edit settings."""
    options = [
        'System Date/Time',  # New combined option
        'Sunrise Time',
        'Sunset Time',
        'Irrigation',
        'Temp Setpoint',
        'Humidity Setpoint',
        'Camera On',
        'Camera Off',
        'Back'
    ]
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
            if options[index] == 'System Date/Time':
                adjust_system_time('System Date/Time')
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
            elif options[index] == 'Camera On':
                config.update_config('PICAMERA', 'CameraSet', '1')
                apply_settings()
            elif options[index] == 'Camera Off':
                config.update_config('PICAMERA', 'CameraSet', '0')
                apply_settings()
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
            return  # Simply return to previous menu
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
    """Function to adjust the system date and time."""
    now = datetime.now()
    current = {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hours': now.hour,
        'minutes': now.minute
    }
    
    # Define field positions and lengths
    fields = {
        'year': (0, 0, 4),    # (col, row, length)
        'month': (5, 0, 2),
        'day': (8, 0, 2),
        'hours': (0, 1, 2),
        'minutes': (3, 1, 2)
    }
    
    current_field = 'year'
    blink_state = True
    last_blink = time.monotonic()
    BLINK_INTERVAL = 0.5  # Blink every half second
    
    # Initial display of full date/time
    lcd.clear()
    date_str = f"{current['year']}/{current['month']:02d}/{current['day']:02d}"
    time_str = f"{current['hours']:02d}:{current['minutes']:02d}"
    lcd.message = f"{date_str}\n{time_str}"
    
    while True:
        current_time = time.monotonic()
        col, row, length = fields[current_field]
        
        # Handle blinking of current field
        if current_time - last_blink >= BLINK_INTERVAL:
            blink_state = not blink_state
            last_blink = current_time
            
            # Update display based on blink state
            if current_field in ['year', 'month', 'day']:
                if current_field == 'year':
                    field_str = f"{current['year']}" if blink_state else "    "
                else:
                    field_str = f"{current[current_field]:02d}" if blink_state else "  "
            else:  # hours or minutes
                field_str = f"{current[current_field]:02d}" if blink_state else "  "
            
            lcd.cursor_position(col, row)
            lcd.message = field_str
            
            # Restore separators if needed
            if not blink_state:
                if current_field in ['year', 'month']:
                    lcd.cursor_position(4 if current_field == 'year' else 7, 0)
                    lcd.message = "/"
                elif current_field == 'hours':
                    lcd.cursor_position(2, 1)
                    lcd.message = ":"
        
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            if current_field == 'year':
                current['year'] = min(current['year'] + 1, 2099)
            elif current_field == 'month':
                current['month'] = min(current['month'] + 1, 12)
            elif current_field == 'day':
                current['day'] = min(current['day'] + 1, 31)
            elif current_field == 'hours':
                current['hours'] = (current['hours'] + 1) % 24
            else:  # minutes
                current['minutes'] = (current['minutes'] + 1) % 60
            
            # Show the new value immediately
            lcd.cursor_position(col, row)
            if current_field == 'year':
                lcd.message = f"{current['year']}"
            else:
                lcd.message = f"{current[current_field]:02d}"
            blink_state = True
            last_blink = current_time
                
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            if current_field == 'year':
                current['year'] = max(current['year'] - 1, 2000)
            elif current_field == 'month':
                current['month'] = max(current['month'] - 1, 1)
            elif current_field == 'day':
                current['day'] = max(current['day'] - 1, 1)
            elif current_field == 'hours':
                current['hours'] = (current['hours'] - 1) % 24
            else:  # minutes
                current['minutes'] = (current['minutes'] - 1) % 60
            
            # Show the new value immediately
            lcd.cursor_position(col, row)
            if current_field == 'year':
                lcd.message = f"{current['year']}"
            else:
                lcd.message = f"{current[current_field]:02d}"
            blink_state = True
            last_blink = current_time
                
        elif lcd.right_button:
            debounce(lambda: lcd.right_button)
            # Restore current field before moving
            lcd.cursor_position(col, row)
            if current_field == 'year':
                lcd.message = f"{current['year']}"
            else:
                lcd.message = f"{current[current_field]:02d}"
            
            if current_field == 'year':
                current_field = 'month'
            elif current_field == 'month':
                current_field = 'day'
            elif current_field == 'day':
                current_field = 'hours'
            elif current_field == 'hours':
                current_field = 'minutes'
            elif current_field == 'minutes':
                current_field = 'year'
            
            blink_state = True
            last_blink = current_time
                
        elif lcd.left_button:
            debounce(lambda: lcd.left_button)
            # Restore current field before moving
            lcd.cursor_position(col, row)
            if current_field == 'year':
                lcd.message = f"{current['year']}"
            else:
                lcd.message = f"{current[current_field]:02d}"
            
            if current_field == 'year':
                current_field = 'minutes'
            elif current_field == 'month':
                current_field = 'year'
            elif current_field == 'day':
                current_field = 'month'
            elif current_field == 'hours':
                current_field = 'day'
            elif current_field == 'minutes':
                current_field = 'hours'
            
            blink_state = True
            last_blink = current_time
            
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            try:
                date_str = f"{current['year']}-{current['month']:02d}-{current['day']:02d}"
                time_str = f"{current['hours']:02d}:{current['minutes']:02d}:00"
                
                subprocess.run(["sudo", "date", "-s", f"{date_str} {time_str}"], check=True)
                subprocess.run(["sudo", "hwclock", "-w"], check=True)
                
                lcd.clear()
                lcd.message = f"{date_str}\n{time_str}"
                time.sleep(2)
                return
                
            except Exception as e:
                lcd.clear()
                lcd.message = "Error Setting\nTime"
                time.sleep(1)
                return
        
        time.sleep(0.05)  # Shorter delay for smoother blinking

def irrigation_menu():
    """Function to navigate and edit irrigation settings."""
    options = [
        'Soil Moist Thresh',
        'View Moisture',     # New option
        'Monitor Live',      # New option
        'Water Vol',
        'Watering Time',
        'Back'
    ]
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
            elif options[index] == 'View Moisture':
                show_current_moisture()
            elif options[index] == 'Monitor Live':
                monitor_moisture()
            elif options[index] == 'Water Vol':
                adjust_parameter('waterVol', 1, 0, 50, 'Water mm of Rain')
            elif options[index] == 'Watering Time':
                adjust_time_parameter('checkTime', 'Watering Time')
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)

def adjust_soil_moisture_threshold():
    """Function to adjust soil moisture threshold as a percentage."""
    cfg = config.read_config()
    value = int(cfg['PLANTCFG']['dryValue'])
    percentage = int((value / 1000) * 100)  # Convert to percentage
    lcd.clear()
    lcd.message = f"Soil Moisture:\n{percentage}%"
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
                lcd.clear()
                lcd.message = f"Soil Moisture:\n{percentage}%"
                last_update = current_time
        elif lcd.down_button:
            if hold_start is None:
                hold_start = current_time
                percentage = max(percentage - 1, 0)
            elif current_time - hold_start > 0.5:  # Hold for 0.5 seconds
                percentage = max(percentage - 10, 0)
            if current_time - last_update > 0.1:  # Update display every 0.1 seconds
                lcd.clear()
                lcd.message = f"Soil Moisture:\n{percentage}%"
                last_update = current_time
        else:
            hold_start = None
        if lcd.select_button:
            debounce(lambda: lcd.select_button)
            value = int((percentage / 100) * 1000)  # Convert back to 0-1000 range
            config.update_config('PLANTCFG', 'dryValue', str(value))
            apply_settings()  # Apply the parameter change
            lcd.clear()
            lcd.message = f"Set to:\n{percentage}%"
            time.sleep(1)  # Show the set message
            return  # Simply return to previous menu instead of clear_and_return_to_menu()
        time.sleep(0.05)  # Reduce CPU usage

def manual_control_menu():
    """Function to handle manual controls."""
    options = [
        'Water Now', 
        'Stop Watering', 
        'Light On Now', 
        'Light Off Now', 
        'Fan On Now', 
        'Fan Off Now',
        'Take Picture Now',
        'Record Data Now',  # New option
        'Back'
    ]
    index = 0
    display_menu(options, index)
    while True:
        if watering_active:
            # If watering is active, ignore all button presses except Stop Watering
            if lcd.select_button and options[index] == 'Stop Watering':
                debounce(lambda: lcd.select_button)
                control_watering(False)
            time.sleep(0.1)
            continue
            
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
            if options[index] == 'Take Picture Now':
                start_picture_thread()
            elif options[index] == 'Water Now':
                start_watering_thread()
            elif options[index] == 'Stop Watering':
                control_watering(False)
            elif options[index] == 'Light On Now':
                control_light(True)
            elif options[index] == 'Light Off Now':
                control_light(False)
            elif options[index] == 'Fan On Now':
                start_fan_thread()
            elif options[index] == 'Fan Off Now':
                control_fan(False)
            elif options[index] == 'Record Data Now':  # Handle new option
                record_data_to_excel()
            elif options[index] == 'Back':
                if not watering_active:  # Only allow back if not watering
                    return
            display_menu(options, index)
            time.sleep(0.5)

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
        set_lcd_color("in_progress")  # Blue while changing light state
        if turn_on:
            result = growlighton()
            manual_override["light"] = True
        else:
            result = growlightoff()
            manual_override["light"] = False
        set_lcd_color("normal")  # Back to normal when done
        lcd.clear()
        lcd.message = ("Light On" if turn_on else "Light Off") if result else "Light Change Failed"
        time.sleep(2)
    except Exception as e:
        set_lcd_color("error")
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)
        set_lcd_color("normal")

def control_picture():
    """Control the picture-taking process."""
    try:
        set_lcd_color("in_progress")
        lcd.clear()
        lcd.message = "Taking Picture..."
        # Don't check buttons during picture capture
        result = picam_capture()
        set_lcd_color("normal")
        lcd.clear()
        lcd.message = "Picture Taken" if result else "Picture Failed"
        time.sleep(2)
    except Exception as e:
        set_lcd_color("error")
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)
        set_lcd_color("normal")

def control_watering(start):
    """Control the watering system."""
    global manual_override, watering_active
    try:
        settings = config.get_plant_settings()
        if start:
            # Clear and set message before starting watering
            lcd.clear()
            set_lcd_color("in_progress")
            lcd.message = "Watering..."
            
            # Start watering
            result = autorain(settings['waterVol'])
            manual_override["watering"] = True
            
            # Only update display after watering is complete
            lcd.clear()
            set_lcd_color("normal")
            lcd.message = "Watering Done" if result == 1 else "Watering Failed"
            watering_active = False
            time.sleep(2)
        else:
            # For manual stop
            lcd.clear()
            set_lcd_color("in_progress")
            result = stopwater()
            manual_override["watering"] = False
            watering_active = False
            
            lcd.clear()
            set_lcd_color("normal")
            lcd.message = "Water Stopped"
            time.sleep(2)
    except Exception as e:
        lcd.clear()
        set_lcd_color("error")
        lcd.message = f"Error: {e}"
        time.sleep(2)
        set_lcd_color("normal")

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
        settings = config.get_plant_settings()
        if turn_on:
            set_lcd_color("in_progress")
            lcd.clear()
            lcd.message = "Starting Fan..."
            result = fanon(settings['fanTime'])
            manual_override["fan"] = True
            # Don't check buttons during fan operation
            lcd.clear()
            lcd.message = "Fan Running..."
            time.sleep(settings['fanTime'])  # Wait for fan cycle
            set_lcd_color("normal")
            lcd.clear()
            lcd.message = "Fan Done" if result else "Fan Failed"
        else:
            set_lcd_color("in_progress")
            result = fanoff()
            manual_override["fan"] = False
            set_lcd_color("normal")
            lcd.clear()
            lcd.message = "Fan Off" if result else "Fan Off Failed"
        time.sleep(2)
    except Exception as e:
        set_lcd_color("error")
        lcd.clear()
        lcd.message = f"Error: {e}"
        time.sleep(2)
        set_lcd_color("normal")

def apply_settings():
    try:
        settings = get_plant_settings()
        
        # For fan control based on temperature/humidity
        if ReadVal[0] > settings['maxTemp'] or ReadVal[1] > settings['maxHumid']:
            set_lcd_color("in_progress")  # Blue while starting fan
            fanon(settings['fanTime'])
            set_lcd_color("normal")  # Back to normal after fan starts
        else:
            set_lcd_color("in_progress")  # Blue while stopping fan
            fanoff()
            set_lcd_color("normal")  # Back to normal after fan stops
            
        # Other settings checks can remain commented out as before
        # if checktimebetween(...):
        #     growlighton()
        # else:
        #     growlightoff()
        
        return
    except Exception as e:
        set_lcd_color("error")
        time.sleep(1)
        set_lcd_color("normal")
        return



# Add a function to convert the mm to pump second.  


def main_menu():
    """Function to navigate between different settings."""
    options = [
        'System Info',  # Keep this as first option
        'Edit Settings', 
        'Manual Control',
        'Soil Moisture',
        'Back'
    ]
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
            if options[index] == 'System Info':
                system_info_menu()  # Call the system info menu instead of show_system_info
            elif options[index] == 'Edit Settings':
                edit_settings_menu()
            elif options[index] == 'Manual Control':
                manual_control_menu()
            elif options[index] == 'Soil Moisture':
                show_soil_moisture()
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)

def system_info_menu():
    """Display system information menu"""
    menu_items = [
        "System Version",
        "Update Firmware",
        "Log Export",
        "Back"
    ]
    index = 0
    display_menu(menu_items, index)
    
    while True:
        update = False
        if lcd.up_button:
            debounce(lambda: lcd.up_button)
            index = (index - 1) % len(menu_items)
            update = True
        elif lcd.down_button:
            debounce(lambda: lcd.down_button)
            index = (index + 1) % len(menu_items)
            update = True
            
        if update:
            display_menu(menu_items, index)
        elif lcd.select_button:
            debounce(lambda: lcd.select_button)
            if menu_items[index] == "System Version":
                show_system_info()
            elif menu_items[index] == "Update Firmware":
                update_firmware_screen()
            elif menu_items[index] == "Log Export":
                export_log_screen()
            elif menu_items[index] == "Back":
                return
            display_menu(menu_items, index)
            time.sleep(0.5)


def show_system_info():
    """Display system version information"""
    try:
        # Read versions using the centralized function
        version_info = get_version_info()
        
        lcd.clear()
        lcd.message = version_info
        
        # Wait for select button press
        while True:
            if lcd.select_button:
                debounce(lambda: lcd.select_button)
                break
            time.sleep(0.1)
            
    except Exception as e:
        lcd.clear()
        lcd.message = "Error reading\nversion info"
        time.sleep(2)

def get_version_info():
    """Get formatted version information string"""
    try:
        # Read from correct paths
        sw_version = readcsv_softver('software_version')  # From Software/code/softver
        fw_version = readcsv('fw_version')  # From Software/userdata/ulnoowegdat
        return f"SW Ver: {sw_version}\nFW Ver: {fw_version}"
    except Exception as e:
        return "Error reading\nversion info"

def show_soil_moisture():
    """Display soil moisture menu and readings"""
    options = [
        'Current Reading',
        'Monitor Values',
        'Show Threshold',
        'Back'
    ]
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
            if options[index] == 'Current Reading':
                show_current_moisture()
            elif options[index] == 'Monitor Values':
                monitor_moisture()
            elif options[index] == 'Show Threshold':
                show_moisture_threshold()
            elif options[index] == 'Back':
                return
            display_menu(options, index)
            time.sleep(0.5)

def show_current_moisture():
    """Display single moisture reading"""
    try:
        from sensorfeed import feedread
        
        lcd.clear()
        lcd.message = "Reading sensor..."
        # Get current reading
        _, _, soil_moisture = feedread()
        
        # Convert to percentage
        moisture_percent = int((soil_moisture / 1000) * 100)
        
        lcd.clear()
        lcd.message = f"Soil Moisture:\n{moisture_percent}% ({soil_moisture})"
        
        # Wait for select button
        while True:
            if lcd.select_button:
                debounce(lambda: lcd.select_button)
                break
            time.sleep(0.1)
            
    except Exception as e:
        lcd.clear()
        lcd.message = "Error reading\nsensor"
        time.sleep(2)

def monitor_moisture():
    """Continuously monitor moisture values"""
    try:
        from sensorfeed import feedread
        
        lcd.clear()
        lcd.message = "Monitoring...\nSelect to exit"
        time.sleep(1)
        
        while True:
            # Get current reading
            _, _, soil_moisture = feedread()
            moisture_percent = int((soil_moisture / 1000) * 100)
            
            # Update display
            lcd.clear()
            lcd.message = f"Live Reading:\n{moisture_percent}% ({soil_moisture})"
            
            # Check for exit
            if lcd.select_button:
                debounce(lambda: lcd.select_button)
                break
                
            # Wait before next reading
            time.sleep(2)
            
    except Exception as e:
        lcd.clear()
        lcd.message = "Error monitoring\nsensor"
        time.sleep(2)

def show_moisture_threshold():
    """Show current moisture threshold setting"""
    try:
        from config import get_plant_settings
        settings = get_plant_settings()
        
        dry_value = settings['dryValue']
        threshold_percent = int((dry_value / 1000) * 100)
        
        lcd.clear()
        lcd.message = f"Dry Threshold:\n{threshold_percent}% ({dry_value})"
        
        # Wait for select button
        while True:
            if lcd.select_button:
                debounce(lambda: lcd.select_button)
                break
            time.sleep(0.1)
            
    except Exception as e:
        lcd.clear()
        lcd.message = "Error reading\nthreshold"
        time.sleep(2)

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

def clear_action_status():
    """Clear the blue action status light"""
    lcd.color = [0, 100, 0]  # Return to green (normal state)
    lcd.rgb = [0, 100, 0]    # Ensure RGB values are set
    lcd.contrast = 40        # Reset contrast to default

def display_status(message, action=False):
    if action:
        lcd.set_color(0.0, 0.0, 1.0)  # Blue for action
    else:
        clear_action_status()

def export_log_screen():
    """Handle log export process"""
    try:
        lcd.clear()
        set_lcd_color("in_progress")  # Blue while exporting
        lcd.message = "Exporting log...\nPlease wait"
        
        # Call logtofile function
        from logoutput import logtofile
        result = logtofile()
        
        # Show result
        lcd.clear()
        if result == 1:
            set_lcd_color("normal")  # Green for success
            lcd.message = "Log exported\nsuccessfully!"
        else:
            set_lcd_color("error")  # Red for error
            lcd.message = "Export failed!\nTry again"
            
        time.sleep(2)  # Show result message
        set_lcd_color("normal")  # Return to normal color
        
    except Exception as e:
        lcd.clear()
        set_lcd_color("error")
        lcd.message = "Error exporting\nlog file"
        time.sleep(2)
        set_lcd_color("normal")

# Add new function to handle firmware update screen
def update_firmware_screen():
    """Handle firmware update process"""
    try:
        lcd.clear()
        set_lcd_color("in_progress")  # Blue while updating
        lcd.message = "Updating Firmware\nPlease wait..."
        
        # Call the firmware update function
        result = updatefw.grobotfwupdate()
        
        # Show result
        lcd.clear()
        if result == 1:
            set_lcd_color("normal")  # Green for success
            lcd.message = "Update success!\nRestart needed"
            time.sleep(2)
            lcd.clear()
            lcd.message = "Press SELECT to\nrestart GroBot"
            
            # Wait for select button
            while True:
                if lcd.select_button:
                    debounce(lambda: lcd.select_button)
                    subprocess.run(['sudo', 'reboot'])
                time.sleep(0.1)
        else:
            set_lcd_color("error")  # Red for error
            lcd.message = "Update failed!\nPress SELECT"
            while True:
                if lcd.select_button:
                    debounce(lambda: lcd.select_button)
                    break
                time.sleep(0.1)
                
    except Exception as e:
        lcd.clear()
        set_lcd_color("error")
        lcd.message = "Error updating\nfirmware"
        time.sleep(2)
        set_lcd_color("normal")

# Add new function to handle data recording
def record_data_to_excel():
    """Record current sensor data to Excel file."""
    try:
        from sensorfeed import feedread
        from dataout import excelout
        
        # Store current light state
        current_light_state = s2.value  # s2 is the light control pin
        
        lcd.clear()
        set_lcd_color("in_progress")
        lcd.message = "Recording data...\nPlease wait"
        
        # Get current readings
        temp, humidity, soil_moisture = feedread()
        
        # Write to Excel
        result = excelout(temp, humidity, soil_moisture)
        
        # Restore light state if it changed
        if s2.value != current_light_state:
            if current_light_state:
                growlighton()
            else:
                growlightoff()
        
        # Show result
        lcd.clear()
        if result == 1:
            set_lcd_color("normal")
            lcd.message = "Data recorded\nsuccessfully!"
        else:
            set_lcd_color("error")
            lcd.message = "Recording failed!\nTry again"
            
        time.sleep(2)
        set_lcd_color("normal")
        
    except Exception as e:
        lcd.clear()
        set_lcd_color("error")
        lcd.message = "Error recording\ndata"
        time.sleep(2)
        set_lcd_color("normal")



