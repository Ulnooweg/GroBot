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
Major change, moved information that should not be replaced with code update to userdata<br/>
Implement standardized error logging output to userdata folder<br/>
Include additional functions to read and write from ulnoowegdata and softver csv file<br/>
Implement grobot-firmware update script<br/>
Bugfixes and additional features

### V1.0.4
Updated header notes and specifications in some code.<br/>
Documentation update.

### V1.0.3
First release version

## Firmware Update
### V1.1-FW
Comment out SystemMaxUse so it is back to default of 4GB log to increasing logging limit and ensure smoother troubleshooting.<br/>
Turn off wifi<br/>
Turn off Bluetooth<br/>
Update grobot systemd unit file to implement restart rate limit<br/>
Removed unused grobotboot systemd process<br/>
