import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

class esc(object):
    def __init__(self):
        _escPins = [6, 7, 8, 9]
        self.ESC = [None]*4
        self.width_temp = [0]*4
        self.range = [0, 1, 2, 3]
        self.tim = pyb.Timer(3, freq = 125)
        for i in self.range:
            self.ESC[i] = self.tim.channel(i+1, pyb.Timer.PWM, pin = pyb.Pin('PC%s'%_escPins[i]))
        self.set_pwm_percent()

    def set_pwm_percent(self, width = [0]*4):
        self.ESC[0].pulse_width_percent(width[0] / 8 + 13 )
        self.ESC[1].pulse_width_percent(width[1] / 8 + 13 )
        self.ESC[2].pulse_width_percent(width[2] / 8 + 13 )
        self.ESC[3].pulse_width_percent(width[3] / 8 + 13 )
