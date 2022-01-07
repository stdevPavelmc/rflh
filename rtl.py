import sys
import numpy as np
from time import sleep
from scipy import signal
from rtlsdr import RtlSdr

class RF(object):
    def __init__(self, ppm):
        # rtl-sdr
        try:
            self.rtl = RtlSdr()
        except:
            print("Are you sure that there is a HackRF One connected?\nI can't find it!")
            sys.exit()

        # setup
        self.rtl.gain = 28.0
        # Warn! samples must be 2^n number, aka 2048 instead of 2k, 512 instead of 500
        self.rtl.sample_rate = 2.048e6
        if ppm != 0:
            self.rtl.freq_correction = ppm
        self.bw = 50
        self.f = 101500000
        self.freq = self.f - 0.512e6
        self.nperseg = 256
        self.bbw = 0
        self.samples = 1.024e6

    def set_freq(self, freq):
        '''
        freq in hz
        We put the freq in the middle of the lower half
        0----*----F----3----4
        '''

        self.freq = freq
        self.f = freq + (self.rtl.sample_rate / 4)
        self.rtl.center_freq = self.f

    def set_bw(self, bw):
        '''
        bw in khz (between 1khz and 3 Mhz)
        '''

        # failsafe
        bw = int(bw)

        # calculate the neede nperseg to get at least N samples in the bw
        if (bw < 1):
            raise ValueError("bw must be greather than 1kHz")
        if (bw > 800e3):
            raise ValueError("bw must be lower than 800 kHz")

        # N is the desired samples in the bw selected
        N = 5
        self.bw = bw * 1000
        self.nperseg = int((self.rtl.sample_rate / self.bw) * (N + 1))
        self.bbw = self.rtl.sample_rate / self.nperseg

        print("Bin bw is {} khz, with {} segments, {} samples in the BW".format(
            int(self.bbw/1e3), self.nperseg, N + 1))

    def set_gain_lna(self, gain):
        self.rtl.gain = gain

    # compat option against hackrf 
    def set_gain_vga(self, gain):
        return True

    # compat option against hackrf
    def amp_on(self):
        return True

    # compat option against hackrf
    def amp_off(self):
        return True

    def get_average(self):

        # get the samples
        samples = self.rtl.read_samples(self.samples)
        freqs, Pxx = signal.welch(
            samples, fs=self.rtl.sample_rate, nperseg=self.nperseg, return_onesided=False)

        # # use matplotlib to estimate and plot the PSD
        # psd(samples, NFFT=8192, Fs=self.rtl.sample_rate /
        #     1e6, Fc=self.rtl.center_freq/1e6)
        # xlabel('Frequency (MHz)')
        # ylabel('Relative power (dB)')
        # show()

        # Shift frequencies by the center frequency during sample stage
        freqs += self.f

        # Use the 'power' formula for dB (10*log10(X))
        # The 'np.abs(Pxx)' is there because 'Pxx' is complex-valued
        adB = 10 * np.log10(np.abs(Pxx))

        # Parse the arrays to get just the needed ones, amplitude and samples
        ampsum = 0
        samples = 0
        index = 0

        start = self.freq - (self.bw/2)
        stop = self.freq + (self.bw/2)
        for fs in freqs:
            if (fs >= start and fs <= stop):
                ampsum += adB[index]
                samples += 1
            index += 1

        # calc mean
        average_db = ampsum / samples
        return average_db

    def bucket(self, s):
        # set the sampling bucket size
        self.samples = s

    def fast(self):
        # set the sampling bucket size
        self.bucket(512e3)

    def close(self):
        # release the hackrf
        self.rtl.close()

if __name__ == "__main__":
    rtl = RF(68)
    rtl.set_freq(145000000)
    rtl.set_bw(50)
    rtl.fast()
    man_level = rtl.get_average()
    # debug
    print("Frequency: 440. MHz, 200 Khz bandwidth")
    print("Mean level: {}".format(man_level))

