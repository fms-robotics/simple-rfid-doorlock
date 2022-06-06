#  simple-rfid-doorlock 
## Background
This repository contains documentation for the new Raspberrypi-powered keycard access control system, which replaces the old Arduino-powered one.
## Installation
### Software
> This section explains how to set up the RPi and the program (Oct 2020)

> Note: Basic Linux knowledge is required to proceed (Oct 2020)

> WARNING: Raspberry Pi OS (Bullseye) has a different [procedure](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/) to do this (Aug 2022)

1. Flash the [Raspberry Pi OS (Buster) img](https://downloads.raspberrypi.org/raspios_oldstable_armhf/images/raspios_oldstable_armhf-2022-09-26/2022-09-22-raspios-buster-armhf.img.xz) to destination SD Card using [Balena Etcher](https://github.com/balena-io/etcher)
2. Create an empty file called `ssh` (no filename extensions) in `boot` partition 
3. Connect the RPi to power and ethernet
4. Open up a shell on your PC, SSH into the Pi using `pi@raspberrypi` and password `raspberry`
5. Run `sudo raspi-config`;  Select `Interfaces Options` and enable `ssh` and `GPIO`; Go to `Boot Options` and select `autologin CLI` 
6. Install `git` and `python3` with `apt-get`
7. Change the directory to home, and clone this repository
8. Move `simple-rfid-door lock/legacy` to `~/411lock`
9. Append `python3 /home/pi/411lock/script.py &; python3 /home/pi/411lock/driver.py` to `.bashrc`
10. Reboot
11. Complete the setup by following the `Hardware` section
### Hardware
> This section explains what cables should connect to the RPi

(TBD.....)

## Using
> This section explains how to create users for the entry system

A RESTful API was used to provide administrative actions. For usage on the endpoints, please refer to function comments in `legacy/script.py`

## The `unstable` foler
- Q: Is there anything in the `unstable` folder?
- A: An untested rewrite which provides support for async I/O. It was a side project from the original one.