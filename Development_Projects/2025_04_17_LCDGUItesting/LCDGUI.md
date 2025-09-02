# GUI Testing
This directory is for testing new builds for a touch screen GUI.

There are three major files for future GUI testing: form.ui, ui_form.py, and widget.py. QT Widget Designer uses form.ui (in C++) to structure a GUI. ui_form.py is the python variant that is generated through software. widget.py is handles logic and functionality. ### ONLY MAKE CHANGES TO widget.py!!! ANY CHANGES MADE TO ui_form.py OR form.ui WILL BE LOST UPON MAKING CHANGES AND SAVING THROUGH QT WIDGET DESIGNER ###. 

# widgetUIqtpython
This is the latest build for the experimental GUI for a touchscreen. Future development plans revolve around the integration of a touch screen that can support all current menus and data streaming.

QtPython community edition will be used for further development of the .ui and .py files. It is highly recommended that changes are made through QT Widget Designer, and other supported applications under its brand.

# portraitGUI
This is the current build compatible with a 2.8 inch touchscreen. Includes raspberrypi_installlist.txt thats logs config changes, installed libraries, etc.