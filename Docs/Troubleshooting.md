# Troubleshooting

## Table of Contents
[Accessing the system log](#accessing-the-system-log)
[USB Drive corruption](#usb-drive-corruption)
[Growth Enclosure Not Working](#growth-enclosure-not-working)


## Accessing the system log
To access the system logs for the GroBot, please first access the terminal either via SSH or otherwise (see [Accessing Terminal (non-SSH)](FAQ.md#accessing-terminal-non-ssh) and [Terminal/SSH Login Password](FAQ.md#terminalssh-login-password)). Then enter the command:
> journalctl -u grobot.service -n 1000 -r
* Scroll using the scroll wheel.
* Press Ctrl+C to exit the log.

## USB Drive corruption
If the USB drive is become corrupted, please:
1. Reformat it into FAT32. On Windows, this can be done via the Raspberry Pi imager then choosing "ERASE" under Operating Systems option.
2. Afterwards, create 3 folders in the FAT32 USB drive. Ensure it is spelled properly in all lower case:
   * pictures
   * data
   * code
3. Follow the steps to reinstall the GroBot software with factory settings in [setup](Setup.md#installingupdating---reset-grobot-to-factory-settings)

## Growth Enclosure Not Working