import Hamlib
import time
import subprocess
from configparser import ConfigParser

# default vars
MINSTEP = 5.0

class Rotor():
    def __init__(self):
        # load config and start the sub-process control if needed
        self.loadconfig()
        self.start_rotor()

        # limits
        self.MIN_AZ = 0
        self.MIN_EL = 0
        self.MAX_AZ = 360
        self.MAX_EL = 90

    def loadconfig(self):
        # load config from the rotor.conf file
        config = ConfigParser()

        config.read('./rotor.conf')
        self.default = config.get('DEFAULT', 'rotor')
        self.model = config.get(self.default, 'model')
        self.device = config.get(self.default, 'device')
        self.options = config.get(self.default, 'options')

    def start_rotor(self):
        # Disable all debug output from Hamlib
        Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)

        # Create rotor object of type net
        # self.rot = Hamlib.Rot(Hamlib.ROT_MODEL_NETROTCTL)
        self.rot = Hamlib.Rot(int(self.model))

        # Setup device
        self.rot.set_conf("rot_pathname", self.device)

        # setup extra options 
        opts = self.options.strip()
        if len(opts) > 0:
            if not (len(opt) % 2):
                print("Strange, options must be in pairs, trying but may fail...")

            pairs = []
            cmds = []
            s = opts.split(' ')
            for i in range(len(s)/2):
                cmd = s[i*2]
                data = s[i*2 + 1]
                if cmd == '-s':
                    cmds.append(['serial-speed', data])
                if cmd == '-C':
                    cmds.append([data.split('=')[0],
                                data.split('=')[1]])

            for (opt, value) in cmds:
                self.rot.set_conf(opt, value)

        # Open rotor
        # The Python bindings for Hamlib does not return anything
        # so we have no knowledge if this was actually successful...
        self.rot.open()

        # get the limits from the rotor
        self.MIN_AZ = float(self.rot.get_conf("min_az"))
        self.MIN_EL = float(self.rot.get_conf("min_el"))
        self.MAX_AZ = float(self.rot.get_conf("max_az"))
        self.MAX_EL = float(self.rot.get_conf("max_el"))

    def set_position(self, az, elv):
        # check limits
        az = min(self.MAX_AZ, max(self.MIN_AZ, az))
        elv = min(self.MAX_EL, max(self.MIN_EL, elv))

        # ask postion
        [aaz, ael] = self.get_position()
        diff = az - aaz
        if abs(diff) <= MINSTEP:
            self.rot.set_position(aaz + (2 * diff), ael)
            time.sleep(0.25)
        self.rot.set_position(az, elv)

        while (abs(aaz - az) > 1):
            time.sleep(1)
            [aaz, ael] = self.get_position()

    def get_position(self):
        pos = self.rot.get_position()
        return pos

    def go_to(self, az, elv=0):
        self.rot.set_position(az, elv)

    def close(self):
        # close all connections
        if  self.rot:
            self.rot.close()

if __name__ == "__main__":
    r = Rotor()
    a = 0
    for az in range(0, 90, 10):
        r.set_position(az, 0)
        (a, e) = r.get_position()
        print("Azimuth, actual: {}, set: {}".format(a, az))

    # park
    r.go_to(0, 0)
    r.close()
