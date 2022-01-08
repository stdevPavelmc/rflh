# RF Light House (rflh)

A python script to use a rotor and a SDR device (RTL-SDR or HackRF One) to measure the RF level around and get a data set and beautiful interactive graphics.

![background noise measurement 145 Mhz](/imgs/145.png) ![background noise measurement 436 Mhz](/imgs/436.png)

WARNING: This repository is new and under construction, you will see some [TODO] & "(work in progress...)" sections/docs yet.

## Motivation

This project born from a friend's challenge to measure the background noise impact on my 70cm satellite band noise floor, from a new 2/3/4G cellular tower that my ISP is setting up 50m away from my antennas and with direct sight.

Soon I realized the true potential of it and it get bigger and feature rich quickly.

## Features

TLDR; you get a tool to plot a web graph and a csv file (data directory) with the plotted data to process as you wish.

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
- Dark graph.

```h
pavel@agathad:~/rflh/$ python3 rflh.py 436 -b 500 -t 8192000 -u -l 40 -k
[...]
```

**Scenario 2:** Unknown digital intruder on the 2m satellite band (145.828 Mhz) ~12khz width, intermitent signal (~ 0.5 seconds pulse interval)

- Will use 15 kHz of bandwidth
- Will use the ppm as we need accurate results and low bandwidth
- Low integration (bucket of ~512 kbytes) to detect fast changing signals & fast sweep
- Fast sweep to allow detection of fast changing signals (default)
- Step of 5 degrees as I'm using a 4x15 el EME yagis with a narrow beamwidth
- Default gain as we are using a +20dB LNA and high gain yagui array.
- Light graph.

```h
pavel@agathad:~/rflh/$ python3 rflh.py 145.828 -b 15 -p 56 -t 512000 -s 5
[...]
```

Graph shows peaks but no defined signal, will sweep again several times to get csv data and process it on MS Excel or LO Calc later (no need for graphs just data)

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
- Dark graph.
- No data, just graph

```h
pavel@agathad:~/rflh/$ python3 rflh.py 145.828 -b 3 -p 56 -t 2048000 -u -l 14 -n
[...]
```

## Author, contributions & code

The author is Pavel Milanes Costa (CO7WT), you can join the team contributing with code fix, improvements, bug reports, ideas, etc. Use te "Issues" tab for that.

This software is Free Software under GPLv3, see [LICENCE](LICENSE.GPLv3); free as in freedom.

If you find this piece of soft usefull and want to support the author with a tip, hardware donation or just a change for a coffee please contact me at pavelmc@gmail.com for instructions.
