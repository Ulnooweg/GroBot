# Setup instructions
This file contains instructions for setting up/building the GroBot hardware and software.

## Hardware
Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details on hardware setup and building instructions.

## Software

### Notice
This section currently only goes through the steps necessary to install/update the GroBot software, assuming that a properly configured Raspbeery Pi OS running inside a GroBot hardware already exist. The steps required to completely install GroBot software onto a fresh Raspberry Pi installation will be published at a later date. Please contact [Ulnooweg Education Centre - Engineering Department](mailto:engineering@ulnooweg.ca) for more details.

### Downloads
1. Download the latest release of the GroBot software from [the release page](https://github.com/TNarakol-UEC/GroBot/releases/latest).
   - The GroBot software file is titled "Release.zip".
   - Release.zip authenticity can be verified, if necessary, by comparing its SHA-256 hash with the hash in "Release.zip.sha256".
2. Extract the zip file content. You should see 2 directory "code" and "systemd_bootfile".

### Installation
1. Shutdown the GroBot.
2. Remove the USB drive from the GroBot Raspberry Pi.
3. Plug in the USB drive to a computer where latest release of GroBot software was extracted to.
4. Navigate to the USB drive and open the folder "code".
5. **Inside the "code" folder, open the file "grobot_cfg.ini" and note down all current settings as this will be reset to default and will have to be rewritten after update.**
6. Delete every existing file in the folder "code" to ensure that there is no old code files that could conflict with the new version.
7. Copy all the content of the folder "code" from the extracted GroBot release zip file to the folder "code" on the USB drive.
8. Using the value noted down in step 5, open "grobot_cfg.ini" and re-enter all values as noted down. Save the file.
9. Remove the USB drive from the computer and reinsert it into the GroBot.

### Testing
This section is for initial testing to ensure that GroBot functions properly after updating its software.
1. Turns the GroBot on. The GroBot LCD should turns on and if the current time is between the sunrise and sunset time (default is 9.30 to 18.30) the LCD light should turn on.
If GroBot does not turns on. Please either attempt to reinstall the sGroBot software again or consult [Troubleshooting](Troubleshooting.md).