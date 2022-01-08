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

The installation of the utilities & python modules are covered in the [Install requisites](INSTALL_REQUISITES.md) document.

### Examples (use cases)

**Scenario 1:** Elevated noise floor on 70cm satellite band on some direction, broadband noise.

- Will use 500 kHz of bandwidth.
- High integration (bucket of ~8 Mbytes)
- Slow scan as signal is noise and will ignore fast changing signals.
- Step of 10 degrees (default)
- High gain as we are measuring noise.
- PPM here is useless as we are sampling the background noise.
- Interactive graph popup

```h
pavel@agathad:~/rflh/$ python3 rflh.py 436 -b 500 -t 8192000 -u -l 40 -i
[...]
```

**Scenario 2:** Unknown digital intruder on the 2m satellite band (145.828 Mhz) ~12khz width, intermitent signal (~ 0.5 seconds pulse interval)

- Will use 15 kHz of bandwidth
- Will use the ppm as we need accurate results and low bandwidth
- Low integration (bucket of ~512 kbytes) to detect fast changing signals & fast sweep
- Fast sweep to allow detection of fast changing signals (default)
- Step of 5 degrees as I'm using a 4x15 el EME yagis with a narrow beamwidth
- Default gain as we are using a +20dB LNA and high gain yagui array.

```h
pavel@agathad:~/rflh/$ python3 rflh.py 145.828 -b 15 -p 56 -t 512000 -s 5
[...]
```

Graph shows peaks but no defined signal, will sweep again several times to get only csv data and process it on MS Excel or LO Calc later (no need for graphs, just data)

```h
pavel@agathad:~/rflh/$ python3 rflh.py 145.828 -b 15 -p 56 -t 512000 -s 5 -j
[...]
```

**Scenario 3:** New [OEM] 6m yagui and need to check the radiation lobes as the datasheet is to good to be true.

Neigbor HAM 800m away will radiate an 2khz wide MT63 transmission for about 2 minutes with 5W on 50.15 Mhz (antenna sweetspot according to the OEM) with his vertical antenna (omni)

- Will use 3 kHz of bandwidth.
- Will use the ppm as we need accurate results and low bandwidth
- Medium integration for accuracy (bucket of ~2 Mbytes)
- Slow scan as signal may vary/reflect
- Step of 10 degrees (default)
- Lower gain as we are measuring a near & powerful signal.
- No data, just graph
- Interactive graph popup

```h
pavel@agathad:~/rflh/$ python3 rflh.py 145.828 -b 3 -p 56 -t 2048000 -u -l 14 -n -i
[...]
```

## Author, contributions, code & donations

The author is Pavel Milanes Costa (CO7WT), you can join the team contributing with code fix, improvements, bug reports, ideas, etc. Use te "Issues" tab for that.

This software is Free Software under GPLv3, see [LICENCE](LICENSE.GPLv3); free as in freedom.

If you find this piece of soft usefull and want to support the author with a tip, hardware donation or just a change for a coffee please contact me at pavelmc@gmail.com for instructions.

For money tips you can use my [QvaPay donation page](https://qvapay.com/payme/pavelmc), thanks in advance!
