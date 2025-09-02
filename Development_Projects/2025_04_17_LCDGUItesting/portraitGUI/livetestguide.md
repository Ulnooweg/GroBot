### Screen Swap
This procedure is for swapping the 16x2 RGB Adafruit LCD with the 2.8inch touchscreen. The hope is that after a screenswap and an sd card swap, testing code migration from v1.2 will be easier to gauge; live feedback would become available.

The basis for this procedure involves one Raspberry Pi 3A+ Board, if nescessary removing the old SD-card, and attaching the touchscreen.

1. Power off the Grobot.
2. Disconnect the power to the Grobot.
3. Unplug the old I2C connector from the 16x2 Adafruit LCD.
4. Replace the SD-card with the one that includes the development GUI.
5. Connect the DSI from the 2.8" touchscreen to the Raspberry Pi 3A+.
6. Lifting the irrigation hat from the Raspberry Pi.
7. Remove the Raspberry Pi from the Grobot Housing.
8. Connect the DSI cable to the DSI slot. DO NOT CONNECT IT TO THE PI CAMERA SLOT.
9. Power it on with only the SD-card and touchscreen connected to verify both are in working order BEFORE connecting it back into the Grobot.
10. Reattach the irrigation hat.
11. Plug in the Grobot power.
12. Turn the Grobot on.