import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

"""
capture values of a 4-channels RC receiver
each channel give a PWM signal with a 125Hz frequency and a 12.5 to 25% duty-cycle
"""
class rc(object):
    def __init__(self):
        _rcPins = [0, 1, 2, 3]
        self.RC = [None]*4
        self.ic_pin = [None]*4
        self.ic = [None]*4
        self.range = [0, 1, 2, 3]
        self.t5 = pyb.Timer(5, prescaler=83, period=0x0fffffff)
        self.ic_start = [0]*4
        self.ic_width = [0]*4
        for i in self.range:
            self.i = i
            self.ic_pin[i] = pyb.Pin('PA%s'%_rcPins[i])
            self.ic[i] = self.t5.channel(i+1, pyb.Timer.IC, pin=self.ic_pin[i], polarity=pyb.Timer.BOTH)
        self.set_callback()

    def ic_cb0(self, tim):
        if self.ic_pin[0].value():
            self.ic_start[0] = self.ic[0].capture()
        else:
            self.ic_width[0] = max(-100, min(100, (self.ic[0].capture() - self.ic_start[0] & 0x0fffffff - 1100)//4-108))

    def ic_cb1(self, tim):
        if self.ic_pin[1].value():
            self.ic_start[1] = self.ic[1].capture()
        else:
            self.ic_width[1] = max(-100, min(100, -((self.ic[1].capture() - self.ic_start[1] & 0x0fffffff - 1100)//4-104)))

    def ic_cb2(self, tim):
        if self.ic_pin[2].value():
            self.ic_start[2] = self.ic[2].capture()
        else:
            self.ic_width[2] = max(0, min(100, -(self.ic[2].capture() - self.ic_start[2] & 0x0fffffff - 1100)//8+100))

    def ic_cb3(self, tim):
        if self.ic_pin[3].value():
            self.ic_start[3] = self.ic[3].capture()
        else:
            self.ic_width[3] = max(-100, min(100, (self.ic[3].capture() - self.ic_start[3] & 0x0fffffff - 1100)//4-104))

    def set_callback(self):
        self.ic[0].callback(self.ic_cb0)
        self.ic[1].callback(self.ic_cb1)
        self.ic[2].callback(self.ic_cb2)
        self.ic[3].callback(self.ic_cb3)

    def get_raw(self):
        return self.ic_width
