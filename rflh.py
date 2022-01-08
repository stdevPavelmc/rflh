import time
import argparse
import os
import matplotlib.pyplot as plt
import random as rnd
from math import pi
from rotor import *

# description
parser = argparse.ArgumentParser(description='Sweep the 360o around recording the signals levels of a frequency at a given bandwidth; using rotctld and a RTL-SDR (default) or a HackRF One for spectrum sensing.')

# frequency
parser.add_argument(
    'frequency',
    type=float,
    help='The center frequency to listen to, in MHz, "145.170" for 145.170 MHz')

# -b / --bandwidth
parser.add_argument(
    '-b ', '--bandwidth',
    type=int,
    help='The bandwidth to sample in kHz: 1-800 kHz using the RTL-SDR or 1kHz-MHz using the HackRF, 20kHz by default')

# -s / --step
parser.add_argument(
    '-s', '--step',
    type=int,
    help='Azimuth steps in degrees, 10 degrees by default, see project README.md for details.')

# -u / --paused
parser.add_argument(
    '-u', '--paused',
    help='Sweep mode: paused mode means move to target azimuth & take a measurement the repeat it (slow). The default is to make one full turn and do measurements on the fly (faster but may fail, read the documentation)',
    action="store_true")

# -bs / --bucketsize
parser.add_argument(
    '-t', '--bucketsize',
    type=int,
    help='Bucket size: how many bytes to get for processing at each sample time, 1.024 Mbytes by default (use 2^n units or it will fail) 1.024 Mbytes = 1024000')

# -p / --ppm
parser.add_argument(
    '-p', '--ppm',
    type=int,
    help='Frequency correction for you device, by default 0.0')

# -q / --quiet
parser.add_argument(
    '-q', '--quiet',
    help='Quiet: supress output, default: verbose',
    action="store_true")

# -j / --just_data
parser.add_argument(
    '-j', '--just_data',
    help='Don\'t generate & save the graph, default: generate & save it',
    action="store_true")

# -n / --nofile
parser.add_argument(
    '-n', '--nofile',
    help='Don\'t save the csv file, default: save it',
    action="store_true")

# -i / --interactive
parser.add_argument(
    '-i', '--interactive',
    help='Pop up a Matplotlib interactive graph with the results, default is no pop up',
    action="store_true")

# -d / --dummy
parser.add_argument(
    '-d', '--dummy',
    help='Don\'t use the rotor or the RTL-SDR or HackRF, just generate a dummy dataset and plot it; it implies --nofile; just for testing purposes',
    action="store_true")

# -l / --lna
parser.add_argument(
    '-l', '--lna',
    type=float,
    help='LNA gain value: 0-49.6 dB in 0.4 dB for the RTL-SDR or 0-40 dB in 8 dB steps for HackRF. Defaults: 28.0 for the RTL-SDR & 32 for the HackRF')

# -v / --vga
parser.add_argument(
    '-v', '--vga',
    type=int,
    help='VGA gain value (Only HackRF One): 0-62 in 2 units steps, 30 by default')

# -a / --amp_on
parser.add_argument(
    '-a', '--amp_on',
    help='Amplifier on (Only HackRF One): by default it\'s disabled; WATCH OUT! some firmware revision has this option reversed (mine has it)',
    action="store_true")

# -o / --hackrfone
parser.add_argument(
    '-o', '--hackrfone',
    help='Use a HackRF One instead the default: RTL-SDR',
    action="store_true")

args = parser.parse_args()

# args setup
fq = float(args.frequency)
bw = 20
if args.bandwidth:
    bw = args.bandwidth

if args.step:
    if args.step < 6:
        print("WARNING: You selected a azimuth step lower/equal than 6 degrees: most rotors can't handle that")
    astep = args.step
else:
    astep = 10

just_data = False
if args.just_data:
    just_data = True

quiet = False
if args.quiet:
    quiet = True

nofile = False
if args.nofile:
    nofile = True

interactive = False
if args.interactive:
    interactive = True

dummy = False
if args.dummy:
    dummy = True

lna_gain = None
if args.lna:
    lna_gain = args.lna

vga_gain = None
if args.vga:
    vga_gain = args.vga

amp_on = False
if args.amp_on:
    amp_on = True

hackrfone = False
if args.hackrfone:
    hackrfone = True

ppm = 0
if args.ppm:
    ppm = args.ppm

# bucketsize
bucketsize = 1.024e6
if args.bucketsize:
    bucketsize = args.bucketsize

paused = False
if args.paused:
    paused = True
elif args.step and args.step <= 5:
    print("WARNING: You selected a step less than 6 degrees & fast scanning, most hardware can\'t handle that!")

# conditional load of the device
if hackrfone:
    from hrf import *
    if not quiet:
        print("Using HackRF One as RF device")
else:
    from rtl import *
    if not quiet:
        print("Using RTL-SDR as RF device")

# instantiating if not testing
if not dummy:
    r = Rotor()
    rf = RF(ppm)

device = 'rtl'
if hackrfone:
    device = 'hackrf'

# array that will hold the data
labels = []
levels = []
f = fq * 1000000
duration = 0

def clean_house():
    if not dummy:
        rf.close()
        r.go_to(0, 0)

# All is wraped to detect Ctrl+c
try:
    # RF setup & rotor parking
    if not dummy:
        # set HackRF
        rf.set_freq(f)
        rf.set_bw(bw)
        rf.bucket(bucketsize)
        if vga_gain != None and hackrfone:
            rf.set_gain_vga(vga_gain)
            if not quiet:
                print("VGA gain set to {}".format(vga_gain))
        if lna_gain != None:
            rf.set_gain_lna(lna_gain)
            if not quiet:
                print("LNA gain set to {}".format(lna_gain))
        if amp_on and hackrfone:
            rf.amp_on()
            if not quiet:
                print("Amp turned on!")

        # rotor parking advice
        if not quiet:
            print("Parking the rotor, please wait...")

        # rotor parking (blocking)
        r.set_position(0, 0)

    # rotor parking advice
    if not quiet:
        if not dummy:
            print("Parking done, starting the sweep")
            print("Sweep for {} Hz ({} MHz) with {} kHz of bandwidth & {} degrees of step.".format(
            f, f/1e6, bw, astep))

    # getting time for the file
    dt = time.strftime("%Y%m%d_%H%M")

    # if dummy data
    if not dummy:
        if paused:
            # slow scanning
            tstart = time.time()
            for p in range(0, 360, astep):
                labels.append(str(p))
                r.set_position(p, 0)
                l = rf.get_average()
                levels.append(l)
                if not quiet:
                    print("{};{}".format(p, str(l).replace(".", ",")))
            
            tstop = time.time()
        else:
            # fast scanning
            a = 0
            at = astep
            tstart = time.time()
            # zero
            labels.append(str(a))
            l = rf.get_average()
            levels.append(l)
            if not quiet:
                print("0(0);{}".format(str(l).replace(".", ",")))
            # start turning!
            r.go_to(360)
            while a < (360 - astep):
                (a, e) = r.get_position()
                if (at - a) < (astep / 2):
                    # data 
                    l = rf.get_average()
                    levels.append(l)
                    (an, e) = r.get_position()
                    am = (an + a) / 2
                    labels.append(str(at))
                    # debug
                    if not quiet:
                        print("{}({});{}".format(at, am, str(l).replace(".", ",")))
                        if (am - at) >= astep:
                            print("ERROR!\n\nThe selected azimuth step is to small or bucket size to big, please adjust them and try again!")
                            clean_house()
                            sys.exit()

                    # increment at
                    at += astep

            tstop = time.time()

        # time elapsed 
        duration = tstop - tstart
        if not quiet:
            print("Scan took {}:{}".format(int(duration/60), int(duration % 60)))

        # Create the name for the file if not told otherwise
        if not nofile:
            dfolder = os.path.join(os.getcwd(), 'data')
            # the data folder exists?
            if not os.path.exists(dfolder):
                os.mkdir(dfolder)
            else:
                if not os.path.isdir(dfolder):
                    os.unlink(dfolder)
                    os.path.mkdir(dfolder)

            # 20211219_2221_rtl_436.5MHz_200kHz_10o.csv
            savefile = "{}_{}_{}MHz_{}kHz_{}o".format(dt, device, fq, bw, astep)
            with open(os.path.join(dfolder, savefile + '.csv'), 'w') as f:
                # write header
                f.writelines("Degrees;dBFs\n")
                i = 0
                for v in labels:
                    f.writelines(str(v) + ";" + str(levels[i]).replace(".", ",") + "\n")
                    i = i + 1

            if not quiet:
                print("CSVFile: data/{}".format(savefile + ".csv"))
    else:
        # fake data
        rnd.seed()
        astep = 5
        units = 360/astep
        labels = [x for x in range(0, 360, astep)]
        start = rnd.randint(-1100, -600)
        stop = rnd.randint(start, 50)
        levels = []
        for l in labels:
            levels.append(rnd.randrange(start, stop)/10.0)

    if not quiet and not dummy:
        print("Parking the rotor in the background")
        clean_house()

    # statistics
    margin = 0.5
    amin = min(levels)
    amax = max(levels)
    tmargin = abs(amax - amin)
    if tmargin < 1:
        margin = 0.5
    else:
        margin = tmargin * 0.1
    lmin = amin - margin
    lmax = amax + margin

    if not quiet:
        print("Dynamc range: {} dB, 10%: {}".format(tmargin, margin))
        print("Min: {}, Max {}".format(lmin, lmax))

    if not just_data:
        speed = 'fast'
        if paused:
            speed = 'paused'

        title = u"{}: ({}: {}) {:.3f} MHz, BW: {:.1f} kHz,\n{}o steps, {:.1f} dB of DNR".format(
            device.upper(),
            speed,
            "{}:{} min".format(
                int(duration / 60),
                int(duration % 60)
            ),
            fq,
            bw,
            astep,
            tmargin
        )

        # Turn interactive plotting off
        plt.ioff()

        # create
        fig = plt.figure()
        ax = fig.add_subplot(label='title')
        fig.subplots_adjust(top=0.85)

        # Set titles for the figure and the subplot respectively
        fig.suptitle(title, fontsize=12, fontweight='normal')

        # repeat the last value to close the plot
        levels += levels[:1]

        # how many ticks/labels on the plot
        N = len(labels)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        # repeat the first one to close the graph
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(111, polar=True, label='graph')

        # Draw one axe per variable + add labels
        plt.xticks(angles, labels, color='grey', size=8)

        # set labels limits
        plt.ylim(lmin, lmax)

        # Plot data
        ax.plot(angles, levels, linewidth=1, linestyle='solid')

        # rotate
        ax.set_theta_zero_location('N')

        # make it clockwise
        ax.set_theta_direction(-1)

        # Fill area
        ax.fill(angles, levels, 'b', alpha=0.1)

        # save only if not dummy
        if not dummy and not just_data:
            plt.savefig(
                os.path.join(dfolder, savefile + '.png'),
                bbox_inches='tight'
            )
            if not quiet:
                print("ImgFile: data/{}".format(savefile + ".png"))

        # Show the graph if instructed to
        if interactive:
            plt.show()

except KeyboardInterrupt:
    print("\n\nCatching Ctrl+C: cleaning the house before leaving...")
    clean_house()
    sys.exit()
