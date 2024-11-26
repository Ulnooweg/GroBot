# Changelog
This file lists all the historical changelogs of the project as published publicly on this Github repository.

## Table of Contents
### Programs Changelogs
[V1.1](#v11)

[V1.0.4](#v104)

[V1.0.3](#v103)

### Firmware Updates
[V1.1](#v11-fw)


## Programs Changelogs
### V1.1
Major change, moved infomation not repalced with code update to userdata
Implement standardized error logging output to userdata folder
Include additional functions to read and write from ulnoowegdata and softver csv file
Implement grobot-firmware update script

### V1.0.4
Updated header notes and specifications in some code.
Documentation update.

### V1.0.3
First release version

## Firmware Update
### V1.1-FW
Comment out SystemMaxUse so it is back to default of 4GB log to increasing logging limit and ensure smoother troubleshooting.
Turn off wifi
Turn off Bluetooth
Update grobot systemd unit file to implement restart rate limit
Removed unused grobotboot systemd process
