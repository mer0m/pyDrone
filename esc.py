import pyb
import micropython
micropython.alloc_emergency_exception_buf(100)

"""
4-channels ESC array
each channel generates a PWM signal with a 125Hz frequency and a 12.5 to 25% duty-cycle (0 to 100 in input)
"""
class esc(object):
    def __init__(self):
        _escPins = [6, 7, 8, 9]
        self.esc_array = [None]*4
        self.tim = pyb.Timer(3, freq = 125)
        
        for i in range(4):
            self.esc_array[i] = self.tim.channel(i+1, pyb.Timer.PWM, pin = pyb.Pin('PC%s'%_escPins[i]))
        self.set_pwm_percent()

    def set_pwm_percent(self, width = [0]*4):
        self.esc_array[0].pulse_width_percent(width[0] / 8 + 13 )
        self.esc_array[1].pulse_width_percent(width[1] / 8 + 13 )
        self.esc_array[2].pulse_width_percent(width[2] / 8 + 13 )
        self.esc_array[3].pulse_width_percent(width[3] / 8 + 13 )
