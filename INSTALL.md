# Install instructions

## Linux

In linux you have a setup script on the project folder named `linux_setup.sh`, it has all the install steps. Just run it like this from a console:

```sh
./linux_setup.sh
```

It will ask for your credentials once and will install all the needed tools, after it finished (with no errors I hope!) you can jump to the test section below.

## Windows [in progress]

I have not experience deploying it on Windows yet (I will try to deploy it and document this later)

## Hamlib rotctld setup

You have a file called rotor.conf in the app folder, there you have some example section for a dummy rotor, a network rotor using hamlib protocol, a Yaesu GS-232A & B models and SPID Rot2Prog one.

Just copy ot modify one of the sections and when finished go to the DEFAULT section and set the 'rotor' var to the name of the rotor you use, in the example the NET rotor is selected.

That's is, the rotor class will handle the config and connection to the rotor specified.

## Testing

Note: This section is focused on linux, I think that the windows testing procedure will not differ much once installed properly as all test instructions uses the same console apps.

### Native RTL-SDR support

Plug your RTL-SDR to the PC and run this on the console. If success this command will hang in there until you press CTRL+C

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
lost at least 180 bytes
```

### Python3 RTL-SDR support

Just run the rtl.py file, like this

```sh
pavel@agathad:~/$ python3 rtl.py
Detached kernel driver
Found Rafael Micro R820T tuner
[R82XX] PLL not locked!
Bin bw is 8 khz, with 245 segments, 6 samples in the BW
Frequency: 440. MHz, 200 Khz bandwidth
Mean level: -104.62619156247725
Reattached kernel driver

```

If you see the `Mean level: -xxx.yyyyyyyyy` line all is fine.

### Native HackRF support

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

If you see some similar info then you have the support already.

### Python3 HackRF support

Just run the hrf.py file, like this

```sh
pavel@agathad:~/$ python3 hrf.py
Bin bw is 8 khz, with 960 segments, 6 samples in the BW
Frequency: 440. MHz, 200 Khz bandwidth
Mean level: -107.43880857116446
Releasing the HackRF One
```

If you see the `Mean level: -xxx.yyyyyyyyy` line all is fine.

### Hamlib rotctld support

For the rotor comms you need to setup your rotor with the hamlib `rotctld` tool to listen in the localhost for instructions, the script will talk to it. See the rotctld configuration section below.

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

## Let's Go!

After testing you have all pieces working it's time to test it for real.

0. Connect all the rotor neded cables.
0. Connect the SDR device to the antenna connected to the rotor and to the PC

Fire a sample runs:

```sh
python3 rflh.py 145.000 -i
```

**Note:** to use the HackRf is just to add the `-o` option to that line.

If all goes well you will see a poping up windows at the end with a graph and have a 'data' folder with the CSV & image files.

Is then time to take a peek on the [explained option](OPTIONS_EXPLAINED.md)