import Hamlib
import time

ELMAX = 72
AZMAX = 360
MINSTEP = 5

class Rotor():
    def __init__(self):
        self.rotorhost = "10.42.1.6"
        self.rotorport = 4533

        # Disable all debug output from Hamlib
        Hamlib.rig_set_debug(Hamlib.RIG_DEBUG_NONE)

        # Create rotor object of type net
        self.rot = Hamlib.Rot(Hamlib.ROT_MODEL_NETROTCTL)

        # Setup network protocol
        self.rot.set_conf("rot_pathname", self.rotorhost + ":" + str(self.rotorport))

        # Open rotor
        # The Python bindings for Hamlib does not return anything
        # so we have no knowledge if this was actually successful...
        self.rot.open()

    def set_position(self, az, elv):
        # Value conditionign
        if az > AZMAX:
            az = AZMAX
        if az < 0:
            az = 0
        if elv > ELMAX:
            elv = ELMAX
        if elv < 0:
            elv = 0

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

if __name__ == "__main__":
    r = Rotor()
    a = 0
    for az in range(0, 95, 10):
        r.set_position(az, 0)
        (a, e) = r.get_position()
        print("Azimuth, actual: {}, set: {}".format(a, az))

    # park
    r.go_to(0, 0)