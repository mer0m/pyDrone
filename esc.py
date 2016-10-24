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

    def set_esc_percent(self, width = [0]*4):
        for i in range(4):
            self.esc_array[i].pulse_width_percent(width[i] / 8 + 13 )
