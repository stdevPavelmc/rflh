import sys
import numpy as np
from time import sleep
from scipy import signal
from libhackrf import *

class RF(object):
    def __init__(self, ppm):
        try:
            self.hrf = HackRF()
        except:
            print("Are you sure that there is a HackRF One connected?\nI can't find it!")
            sys.exit()
        
        # HackRF setup
        self.hrf.lna_gain = 32
        self.hrf.vga_gain = 30
        self.hrf.sample_rate = 8e6
        #self.hrf.freq_correction = ppm #TODO
        self.bw = 50
        self.f = 101500000
        self.freq = self.f - 2e6
        self.nperseg = 256
        self.bbw = 0
        self.samples = 1.024e6

        # enable/disable the built-in amplifier:
        #self.hrf.enable_amp()
        self.hrf.disable_amp()

    def set_freq(self, freq):
        '''
        freq in hz
        We put the freq in the middle of the lower half
        0----*----F----3----4
        '''

        self.freq = freq
        self.f = freq + (self.hrf.sample_rate / 4)
        self.hrf.center_freq = self.f

    def set_bw(self, bw):
        '''
        bw in khz (between 1khz and 3 Mhz)
        '''

        # failsafe
        bw = int(bw)

        # calculate the neede nperseg to get at least N samples in the bw
        if (bw < 1):
            raise ValueError("bw must be greather than 1khz")
        if (bw > 3e3):
            raise ValueError("bw must be lower than 3 Mhz")

        # N is the desired samples in the bw selected
        N = 5
        self.bw = bw * 1000
        self.nperseg = int((self.hrf.sample_rate / self.bw) * (N + 1))
        self.bbw = self.hrf.sample_rate / self.nperseg

        print("Bin bw is {} khz, with {} segments, {} samples in the BW".format(
            int(self.bbw/1e3), self.nperseg, N + 1))

    def set_gain_lna(self, gain):
        self.hrf.lna_gain = gain

    def set_gain_vga(self, gain):
        self.hrf.vga_gain = gain

    def amp_on(self):
        self.hrf.enable_amp()

    def amp_off(self):
        self.hrf.disable_amp()

    def get_average(self):

        # get the samples
        samples = self.hrf.read_samples(self.samples)
        freqs, Pxx = signal.welch(
            samples, fs=self.hrf.sample_rate, nperseg=self.nperseg, return_onesided=False)

        # # use matplotlib to estimate and plot the PSD
        # psd(samples, NFFT=8192, Fs=self.hrf.sample_rate /
        #     1e6, Fc=self.hrf.center_freq/1e6)
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

    def fast(self):
        # do a fast scan, just 512k samples
        self.bucket(512e3)

    def bucket(self, s):
        # set the sampling bucket size
        self.samples = s

    def close(self):
        # release the hackrf
        self.hrf.close()

if __name__ == "__main__":
    hrf = RF(0)
    hrf.set_freq(446000000)
    hrf.set_bw(50)
    man_level = hrf.get_average()
    # debug
    print("Frequency: 440. MHz, 200 Khz bandwidth")
    print("Mean level: {}".format(man_level))

