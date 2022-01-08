# Options Explained

This file details the technical aspects of the options and some related low level stuff.

The full feature and option list is given on the console runnig the script with `-h` or `--help` to show them:

```sh
pavel@agathad:~/rflh$ python3 rflh.py  -h
usage: rflh.py [-h] [-b  BANDWIDTH] [-s STEP] [-u] [-t BUCKETSIZE] [-p PPM] [-q] [-j] [-n] [-d] [-l LNA] [-v VGA] [-a] [-o] [-k] frequency

Sweep the 360 degrees around recording the levels of a frequency at a given bandwidth; using rotctld and a RTL-SDR (default) or a HackRF One for spectrum sensing.

positional arguments:
  frequency             The center frequency to listen to, in MHz, "145.170" for 145.170 MHz

optional arguments:
  -h, --help            show this help message and exit
  -b  BANDWIDTH, --bandwidth BANDWIDTH
                        The bandwidth to sample in kHz: 1-800 kHz using the RTL-SDR or 1kHz-MHz
                        using the HackRF, 20kHz by default
  -s STEP, --step STEP  Azimuth steps in degrees, 10 degrees by default, see project README.md
                        for details.
  -u, --paused          Sweep mode: paused mode means move to target azimuth & take a measurement
                        the repeat it (slow). The default is to make one full turn and do
                        measurements on the fly (faster but may fail, read the documentation)
  -t BUCKETSIZE, --bucketsize BUCKETSIZE
                        Bucket size: how many bytes to get for processing at each sample time,
                        1.024 Mbytes by default (use 2^n units or it will fail) 1.024 Mbytes = 1024000
  -p PPM, --ppm PPM     Frequency correction for you device, by default 0.0
  -q, --quiet           Quiet: supress output, default: verbose
  -j, --just_data       Don't generate the web graph, default: generate it
  -n, --nofile          Don't save the csv file, default: save it
  -d, --dummy           Don't use the rotor or the RTL-SDR or HackRF, just generate a dummy
                        dataset and plot it; it implies --nofile; just for testing purposes
  -l LNA, --lna LNA     LNA gain value: 0-49.6 dB in 0.4 dB for the RTL-SDR or 0-40 dB in 8 dB
                        steps for HackRF. Defaults: 28.0 for the RTL-SDR & 32 for the HackRF
  -v VGA, --vga VGA     VGA gain value (Only HackRF One): 0-62 in 2 units steps, 30 by default
  -a, --amp_on          Amplifier on (Only HackRF One): by default it's disabled; WATCH OUT!
                        some firmware revision has this option reversed (mine has it)
  -o, --hackrfone       Use a HackRF One instead the default: RTL-SDR
  -k, --dark            Graph mode: dark (light by default)

pavel@agathad:~/rflh$ 
```

## SDR devices

By default it detect and uses the first RTL-SDR device detected, but if you need to use a HackRF One just issue the `-o` or `--hackrfone` switch and it will look for that device instead.

**RTL-SDR:** it's the default, the script will look for a rtl-device and complain if none is found. Requires pyrtlsdr installed and rtl-sdr support on your PC, see [Install requisites](INSTALL_REQUISITES.md) for more details.

The RTL-SDR device is used with a 2.04 Mhz of bandwidth and only the left half is used, discarding the left-most part of this spectrum slice as it has reduced accuracy it will allow you to sample up to 800 kHz of the spectrum at once.

**HackRF One:** you must select it with the `-o` or `--hackrfone`, the script will look for a rtl-device and complain if none is found. You need support for the HackRF One on your PC, see [Install requisites](INSTALL_REQUISITES.md) for more details.

The HackRF One device is used with at the native 8 Mhz of bandwidth and only the left half is used, discarding the left-most part of this spectrum slice as it has reduced accuracy it will allow you to sample up to 3 MHz of the spectrum at once.

## Bandwidth

You can use the `-b` option to select from 1-800 kHz using the RTL-SDR and from 1 kHz to 3 MHz using the HackRF One. The default is 20 kHz.

We use a pre-calculated bin size to get at least 6 bins for the bandwidth of your selection.

## Azimuth step

By default we use 10 degrees of step, but you can select a lower value. Most rotor has a minimum step of 5 degrees.

This selection interacts with the [Sweep Mode](#sweep-mode) & [Bucket size](#bucket-size) options, see below.

## Sweep mode

The sweep mode by default is fast, TLDR: we force the rotor to go to az=0 & el=0 (park/start position) and then order it to go to az=360 & el=0; we keep track of the current position and launch measurements as needed without stopping the rotor.

**Note:** That measurements have a given [Bucket size](#bucket-size) and the bigger the longer it will take to process it, that can spoil the fast mode.

Depending on your rotor turning speed and hardware processing power to handle the bucket size, the sweep will complete or fail with an error complaining that the azimuth step is to short.

If the bucket size took to long to process and the next position is over the next target position it will fail.

In this scenario the azimuth step & bucket size depends entirely on your hardware, if you get fails with the needed parameters, then you must try the paused/slow mode.

On paused sweep mode, we make blocking calls to the rotor to move to a ceirtain poisition, once we get there we take measurements and then move to the next position (remmember: blocking call); yes this mode is slow, around 3x slower than the fastmode on my hardware.

For example in fastmode and 5 degrees my hardware took 55 seconds, and 3 min 48 seconds on paused sweep mode. (bucket size of 512k)

## Bucket size

That's the amount of data to collect for a given spectrum sampling, by default 1.024 Mbytes will be collected.

You can tune this parameter to your needs for example lower it to detect fast peaks or make it bigger for long integration periods to sample steady but low signals.

It interacts with the fast sweep mode, as the bigger the longer the PC took to process the samples and that can spoil the fast (default) sweep mode.

## PPM error

Almost all SDR devices has a ppm error on the internal clock signal (most cheap RTL-SDR has it) you need to characterize the ppm error of your device and suply it here, can be a negative value and by default it's assumed 0.0 ppm units.

If you are sampling bandwidth of more than ~50 khz you can ignore the ppm correction as it's useles on that scenarios.

But if you are using lower bandwidth and particullary with high bucket sizes you need a ppm correction for precise measurements.

## Just data

As it's name implies it does not generate the pandas dataset and corresponding web visualization at the end of the sweep. The `just data` option is good to use on no GUI envs or networked ones, as a headless Raspberry Pi or other SBC.

## No file

This option will stop the CSV file creation with the data for the sweep. Useful when you are just testing and don't mind the datasets creation at the end of the sweep.

## Dummy data

This option is to test the plotting options and only used on the developing stage.

## LNA (Low noise amplifier) Gain

This option sets the LNA amplification for the selected SDR device, take into account that the LNA levels are discrete values, the corresponding lib will truncate the valued you pased to the nearest possible value.

**RTL-SDR LNA levels**

- Valid Gain levels: 0.0 to 49.6 dB
- Step is 0.4 dB

**HackRF One LNA levels**

- Valid Gain levels: 0.0 to 40.0 dB
- Step is 8.0 dB

By default we set them at my sweetspot levels range for each device in my exprience:

- RTL-SDR: 28.0 dB
- HackRF One: 32.0 dB

## VGA gain (Only for the HackRF)

The VGA gain is a unique feature of the HackRF One, it goes from 0.0 to 62.0 dB in 2.0 dB steps. By default it's set to 30.0 dB

## AMP On (Only for the HackRF)

The `amp on` is a unique feature of the HackRF One, it's an internal, but it has a trick:

On some hardware revisions its function is inverted! Yes, when you turn on the amplifier in software it got shut off in the hardware, weird.

You have to check on your particular device the effects of this switch. My hardware has it reversed, so I shut it off by default (aka: turned on bu default)

## Dark graphs (why not?)

The plotly graph generated is by default themed light, but you can theme it dark to match your site, like this:

![background noise measurement 145 Mhz](/imgs/145.png) ![background noise measurement 436 Mhz](/imgs/436.png)

