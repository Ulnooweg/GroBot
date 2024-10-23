# Setup instructions
This file contains instructions for setting up/building the GroBot hardware and software.

## Hardware
Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details on hardware setup and building instructions.

## Software

### Notice
This section currently only goes through the steps necessary to install/update the GroBot software, assuming that a properly configured Raspbeery Pi OS running inside a GroBot hardware already exist. The steps required to completely install GroBot software onto a fresh Raspberry Pi installation will be published at a later date. Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details.

**There are currently 2 separate installation methods for the GroBot software. The first one will keep all user settings while the second one will reset it to factory settings. Please choose appropriately.**

### Installing/Updating - keeping user settings intact
This instruction set will install/update the GroBot software while keeping user settings intact.
**Please fully read all instructions carefully before implementing them.**

#### Downloads
1. Download the latest release of the GroBot software from [the release page](https://github.com/TNarakol-UEC/GroBot/releases/latest).
   - Download the file titled "Release-keepsettings.zip".
2. Extract the zip file content. You should see a directory called "Release-keepsettings" containing 2 directory "code" and "systemd_bootfile".

#### Installation
1. Shutdown the GroBot.
2. Remove the USB drive from the GroBot Raspberry Pi and plug it in to the computer.
3. Navigate to the USB drive and open the folder "code".
4. Inside the "code" folder, delete every existing file and folder **except grobot_cfg.ini** in the folder "code" to ensure that there is no old code files that could conflict with the new version. Keep "grobot_cfg.ini" to ensure user settings are saved.
   - If there is no "grobot_cfg.ini" in the code folder or it is empty already, please instead use [Installing/Updating - reset GroBot to factory settings](#installingupdating---reset-grobot-to-factory-settings) instructions instead.
5. Copy all the content of the folder "code" from the extracted GroBot Release-keepsettings zip file to the folder "code" on the USB drive.
6. Remove the USB drive from the computer and reinsert it into the GroBot.

#### Testing
This section is for initial testing to ensure that GroBot functions properly after updating its software.
1. Turns the GroBot on. The GroBot LCD should turns on and if the current time is between the sunrise and sunset time (default is 9.30 to 18.30) the LCD light should turn on.
If GroBot does not turns on. Please either attempt to reinstall the GroBot software again or consult [Troubleshooting](Troubleshooting.md).

### Installing/Updating - reset GroBot to factory settings
This instruction set will install/update the GroBot software and reset its setting to factory defaults.
**Note: All settings will be reverted to factory defaults. This action is irreversible**

#### Downloads
1. Download the latest release of the GroBot software from [the release page](https://github.com/TNarakol-UEC/GroBot/releases/latest).
   - Download the file titled "Release.zip".
2. Extract the zip file content. You should see a directory called "Release" containing 2 directory "code" and "systemd_bootfile".

#### Installation
1. Shutdown the GroBot.
2. Remove the USB drive from the GroBot Raspberry Pi and plug it in to the computer.
3. Navigate to the USB drive and open the folder "code".
4. Inside the "code" folder, delete every existing file and folder in the folder "code" to ensure that there is no old code files that could conflict with the new version. 
5. Copy all the content of the folder "code" from the extracted GroBot Release zip file to the folder "code" on the USB drive.
6. Remove the USB drive from the computer and reinsert it into the GroBot.

#### Testing
This section is for initial testing to ensure that GroBot functions properly after updating its software.
1. Turns the GroBot on. The GroBot LCD should turns on and if the current time is between 9.30 and 18.30, the LCD light should turn on.
If GroBot does not turns on. Please either attempt to reinstall the GroBot software again or consult [Troubleshooting](Troubleshooting.md).
