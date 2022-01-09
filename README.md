# RF Light House (rflh)

A python script to use a rotor and a SDR device (RTL-SDR or HackRF One) to measure the RF level around and get a data set and beautiful interactive graphics.

![background noise measurement 145 Mhz](/imgs/145.png)

WARNING: This repository is new and under construction, you will see some [TODO] & "(work in progress...)" sections/docs yet.

## Motivation

This project born from a friend's challenge to measure the background noise impact on my 70cm satellite band noise floor, from a new 2/3/4G cellular tower that my ISP is setting up 50m away from my antennas and with direct sight.

Soon I realized the true potential of it and it get bigger and feature rich quickly.

## Features

At the end of the execution you get:

- A cvs file in the data folder with the resulting data
- A png image in the data folder with the rose plot

Both files are named as follows: `YYYMMDD_HHMM_device_freqMHz_BWkHz_stepo` with the matching .csv and .png extensions. The runtime text on the console name the files created for easy parsing (unless you select the 'quiet' option)

For example a real fast scan showing the references to the img & cvs file for parsing:

```
310(307.5);-102,16941998017171
320(317.5);-101,77656601734243
330(327.5);-101,55990296468812
340(337.5);-101,583492037594
350(347.5);-102,01302571365707
Scan took 0:53
CSVFile: data/20220108_1357_rtl_145.17MHz_300kHz_10o.csv
Parking the rotor in the background
Reattached kernel driver
Dynamc range: 2.9333941135273136 dB, 10%: 0.2933394113527314
Min: -104.78663648956817, Max -101.26656355333539
ImgFile: data/20220108_1357_rtl_145.17MHz_300kHz_10o.png
```

You can stop the generation of the cvs and the image files if not needed, take a peek on the options.

Also if you are on a GUI enviroment you can issue the '-i' or '--interactive' switch and at the end of the sweep a interactive matplotlib graph will popup.

For a more detailed technical stuff on the features see [OPTIONS_EXPLAINED.md](OPTIONS_EXPLAINED.md) (work in progress...)

## Installation

As any script in python you will need some dependencies, default dev env is Ubuntu Linux 20.04 LTS. I'm working/testing a single portable file for linux/windows/mac but it's not ready yet (pyinstall stuff)

The installation of the utilities & python modules are covered in the [Install](INSTALL.md) document.

At the end of the we have some examples / use cases at the end of the [OPTIONS_EXPLAINED.md](OPTIONS_EXPLAINED.md) document.

## Author, contributions, code & donations

The author is Pavel Milanes Costa (CO7WT), you can join the team contributing with code fix, improvements, bug reports, ideas, etc. Use te "Issues" tab for that.

This software is Free Software under GPLv3, see [LICENCE](LICENSE.GPLv3); free as in freedom.

If you find this piece of soft usefull and want to support the author with a tip, hardware donation or just a change for a coffee please contact me at pavelmc@gmail.com for instructions.

For money tips you can use my [QvaPay donation page](https://qvapay.com/payme/pavelmc), thanks in advance!
