# Options Explained

This file details the technical aspects of the options and some related low level stuff.

## SDR devices

**RTL-SDR:** it's the default, the script will look for a rtl-device and complain if none is found (requires pyrtlsdr installed, see Requirements below)

The RTL-SDR device is used with a 2.04 Mhz of bandwidth and only the left half is used, discarding the left-most part of the spectrum as it has reduced accuracy it will allow you to sample up to 800 kHz of the spectrum at once.

**HackRF One:** you must select it with the `-o` or `--hackrfone`, the script will look for a rtl-device and complain if none is found.

The HackRF One device is used with at the native 8 Mhz of bandwidth and only the left half is used, discarding the left-most part of the spectrum as it has reduced accuracy it will allow you to sample up to 3 MHz of the spectrum at once.

## Bandwidth

You can use the `-b` option to select from 1-800 kHz using the RTL-SDR and from 1 kHz to 3 MHz using the HackRF One. The default is 20 kHz.

We use a pre-calculated bin size to get at least 6 bins for the bandwidth of your selection.

## Azimuth step

By default we use 10 degrees of step, but you can select a lower value.

This selection interacts with the [Sweep Mode](#sweep-mode) & [Bucket size](#bucket-size) options, see below.

## Sweep mode

The sweep mode by default is fast, aka: we force the rotor to go to az=0 & el=0 (park/start position) and then order it to go to az=360 & el=0; we keep track of the current position and launch measurements as needed.

That measurements have a given [Bucket size](#bucket-size) and the bigger the longer it will take to process it.

Depending on your rotor speed and hardware processing to handle the bicket size, the sweep will complete or fail with an error complaining that the azimuth step is to short.

In this scenario the particular azimuth step you need depends on that factors, if you get fails with the needed parameters, the you must try paused mode.

On paused sweep mode, we make blocking calls to the rotor to move to a ceirtain poisition, once we get there we take measurements and keep moving to the next position (blocking call); yes this mode is slow, around 3x slower than the fastmode.

For example in fastmode and 5 degrees my hardware took 55 seconds, and 3 min 48 seconds on paused sweep mode.