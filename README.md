# RF Light House (rflh)

A python script to use a rotor and a SDR device (RTL-SDR or HackRF One) to measure the RF level around and get a data set and beautiful interactive graphics.

![background noise measurement 145 Mhz](/imgs/145.png) ![background noise measurement 436 Mhz](/imgs/436.png)

WARNING: This repository is new and under construction, you will see some [TODO] & "(work in progress...)" sections/docs yet.

## Motivation

This project born from a friend's challenge to measure the background noise impact on my 70cm satellite band noise floor, from a new 2/3/4G cellular tower that my ISP is setting up 50m away from my antennas and with direct sight.

Soon I realized the true potential of it and it get bigger and feature rich.

## Features

TLDR; you get a tool to plot a graph and a csv file with the plotted data to process as you wish.

The full feature and option list is given on the console runnig the script with `-h` or `--help` to show them.

For a more detailed technical stuff on the features see [OPTIONS_EXPLAINED.md](OPTIONS_EXPLAINED.md) (work in progress...)


## Installation

As any script in python you will need some dependencies, default dev env is Ubuntu Linux 20.04 LTS, I'm testing a single portable file for linux/windows/mac but it's not ready yet (pyinstall stuff, [TODO])

- Python 3.6 or bigger
- pandas, numpy, pyrtlsdr & scipy modules installed
- rtlsdr or hackrf support on your system (depending on the device you have)
- hamlib support in your system

The installation of this modules and utilities is out of the scope of this document, google it. [TODO: dedicated config details]

### Testing for support

Once you have rtl-sdr or hackrf support you can run the `rtl.py` or the `hrf.py` files directly to test if device comms is working, for example for the rtl-sdr

```sh
pavel@agathad:~/rflh/$ python3 rtl.py 
Detached kernel driver
Found Rafael Micro R820T tuner
[R82XX] PLL not locked!
Bin bw is 8 khz, with 245 segments, 6 samples in the BW
Frequency: 440. MHz, 200 Khz bandwidth
Mean level: -102.59626714939752
Reattached kernel driver
pavel@agathad:~/rflh/$
```

If you see the `Mean level: -xx.yyy` message and no error is present you have a working device. (the same is applicable to the hackrf one)

For the rotor comms you need to setup your rotor with the hamlib `rotctld` tool to listen in the localhost for instructions, the script will talk to it.

To test the rotor run the `rotor.py` script and you will get a result like this (please allow some time to the rotor to move to the 0, 0 position)

```sh
pavel@agathad:~/rflh/$ python3 rotor.py 
Azimuth, actual: 0.0, set: 0
Azimuth, actual: 10.0, set: 10
Azimuth, actual: 20.0, set: 20
Azimuth, actual: 30.0, set: 30
Azimuth, actual: 40.0, set: 40
Azimuth, actual: 50.0, set: 50
Azimuth, actual: 60.0, set: 60
Azimuth, actual: 70.0, set: 70
Azimuth, actual: 80.0, set: 80
Azimuth, actual: 90.0, set: 90
pavel@agathad:~/rflh/$
 ```

Unfortunately the rotor interface on hamlib has no error or feedback if you configured your rotor badly.

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
