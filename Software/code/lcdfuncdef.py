#Copyright 2023-2025 Ulnooweg Education Centre. All rights reserved.
#Licensed under the EUPL-1.2 or later
#
#Source: https://github.com/Ulnooweg/GroBot
#Contact: engineering@ulnooweg.ca
#
########################################
#
#GroBot
#Code: lcdfuncdef
#Version: 1.2
#Description: This is the code containing some lcd control function, split off from lcddispfunc to prevent circular imports.
#Function: TBD
#Input: NONE
#Output: NONE
#Error Handling: Standard UEC Error Handling V1
#
########################################
#Imports
from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C

#Define the LCD object
lcd = Character_LCD_RGB_I2C(i2c, 16, 2)

def set_lcd_color(status):
    try:
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
        else:
            raise RuntimeError('ERR LCD COLOUR SET STRINGS')
        
    except Exception as errvar:
        subprocess.run("(sleep 3 && echo grobot | sudo -S shutdown -r now) &", shell=True)
        lcd.color = [100, 0, 0] #As this code is part of the lcd colour function, needs to explicitly set colour instead of calling the function
        lcd.rgb = [100, 0, 0]  #As this code is part of the lcd colour function, needs to explicitly set colour instead of calling the function
        raise Warning(f"{type(errvar).__name__}({errvar}) in {__file__} at line {errvar.__traceback__.tb_lineno}") from None