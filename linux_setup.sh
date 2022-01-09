#!/bin/bash

# Setup script for any debian based distro (Debian, Ubuntu, Min, etc)

# update package database
sudo apt update

# install python3 ans requisites
sudo apt install -y python3 python3-pip

# install rtl-sdr native support
sudo apt install -y librtlsdr0 rtl-sdr librtlsdr-dev libusb-1.0-0

# install python rtlsdr support
pip3 install pyrtlsdr

# install hackrf native support
sudo apt install -y libhackrf0 libhackrf-dev hackrf

# install support for hamlib (rotctld) python included
sudo apt install -y libhamlib2 libhamlib-utils python3-libhamlib2 

# install app dependencies
pip3 install matplotlib numpy scipy

# end
echo "Done!"