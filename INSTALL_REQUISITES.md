# Install requisites

This document is just a reference for the python modules & device install with some tips and checks

## Python 3

This software is developed under Ubuntu Linux 20.04 LTS with Python v3.8, but I have tested it ok with python 3.6.

You need to have python installed on your path whatever is your OS.

## Linux

Any modern linux distro has it just by calling `python3` but you will need pip3 to install some python modules, just do this on your console:

```sh
sudo apt update && sudo apt install python3-pip
```

### Windows

Just follow this great [tutorial](https://python.tutorials24x7.com/blog/how-to-install-python-3-8-on-windows) by "Tutorials_24x7"

### MacOS

Google it, no MacOS experience here.

## RTL-SDR support

This section is different for each OS, I only have experience on Linux for now:

### Linux

On Debian based distros is simple, just run this:

```sh
sudo apt update && sudo apt install librtlsdr0 rtl-sdr librtlsdr-dev libusb-1.0-0
```

After providing your credentials it will install the needed system libs and apps, to test this just plug in your RTL-SDR and run this (you will get a similar output if success, press `Ctrl+C` to stop it)

```sh
pavel@agathad:~/$ rtl_test 
Found 1 device(s):
  0:  Realtek, RTL2838UHIDIR, SN: 00000001

Using device 0: Generic RTL2832U OEM
Detached kernel driver
Found Rafael Micro R820T tuner
Supported gain values (29): 0.0 0.9 1.4 2.7 3.7 7.7 8.7 12.5 14.4 15.7 16.6 19.7 20.7 22.9 25.4 28.0 29.7 32.8 33.8 36.4 37.2 38.6 40.2 42.1 43.4 43.9 44.5 48.0 49.6 
[R82XX] PLL not locked!
Sampling at 2048000 S/s.

Info: This tool will continuously read from the device, and report if
samples get lost. If you observe no further output, everything is fine.

Reading samples in async mode...
Allocating 15 zero-copy buffers
lost at least 4 bytes

```

### Python RTL-SDR support

You need to install the python3 module `pyrtlsdr`, in your console do this:

```sh
pip3 install pyrtlsdr
```

### Windows [TODO]

### MacOS [TODO]

## HackRF support

This section is different for each OS, I only have experience on Linux for now:

### Linux

On Debian based distros is simple, just run this:

```sh
sudo apt update && sudo apt install libhackrf0 libhackrf-dev hackrf
```

To test the support just plug the HackRF One and run this on your console:

```sh
pavel@agathad:~/$ hackrf_info
hackrf_info version: 2021.03.1
libhackrf version: 2021.03.1 (0.6)
Found HackRF
Index: 0
Serial number: 0000000000000000QRSTUVWXYZ
Board ID Number: 2 (HackRF One)
Firmware Version: 2021.03.1 (API:1.04)
Part ID Number: 0xa0000000 0x005e0000
pavel@agathad:~/$
```

If you see some similar info then you have the support already. There is no need to install python3 support as it's built in on rflh.

### Windows [TODO]

### MacOS [TODO]

## Hamlib (rotor control)

This section is different for each OS, I only have experience on Linux for now:

### Linux

On Debian based distros is simple, just run this:

```sh
sudo apt update && sudo apt install libhamlib2 libhamlib-utils python3-libhamlib2
```

### Windows [TODO]

### MacOS [TODO]

## Configuring rotctld

The way to interface with the rotor is via TCP/IP over localhost on port 4532 (rotctld default)

Basically you need to identify your rotor type, run `rotctl -m` in the console and identify the ID of your rotor, for example the ID of a Yaesu GS-232A compatible rotor is 601

Next you need to now what is the serial device of your rotor, for a default RS-232 connector in your motherboard it's usually `/dev/ttyS0` and `/dev/ttyUSB0` for the first USB-Serial adapter...

To test your rotor communication do this on your console (Yaesu GS-232A compatible rotor on Motherboard RS-232 port) `p` is the "request actual position" command

```sh
rotctl -m 601 /dev/ttyS0 p
```

If all works you will see a respose of the actual position, to test the command just do this (`P 90.0, 0.0` is the command part):

```sh
rotctl -m 601 /dev/ttyS0 P 90.0, 0.0
```

This will move your rotor to 90 degrees of azimuth and 0 elevation.

Then it's just a matter to start the rotctld in a separate console to start the TCP/IP interface *with the same parameters you used*, but without the command part, like this for example:

```sh
rotctld -m 601 /dev/ttyS0
```

**Note:** Maybe you will need to tweak the syntax a little as every rotor has his own details.

See "Testing for support" section below for an example on how to test the rotor control.

## Python needed modules

On any linux just skip the follow Windows only step:

You need to find the pip3 executable to call, check this Stack Overflow [question](https://stackoverflow.com/questions/41501636/how-to-install-pip3-on-windows) about that issue.

On your console (any OS) type this:

```
pip3 install pyrtlsdr plotly pandas numpy scipy
```

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

## Run

You are ready to run it!