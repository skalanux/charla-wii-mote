#!/bin/bash

sudo modprobe uinput
sudo modprobe evdev
sudo mkdir /dev/misc
sudo ln -s /dev/input/uinput /dev/misc/uinput
sudo chmod 666 /dev/misc/uinput
