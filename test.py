import pyb, micropython, esc, rc
micropython.alloc_emergency_exception_buf(100)

esc = esc.esc()
rc = rc.rc()
pyb.Timer(2,freq=100).callback(lambda t:esc.set_pwm_percent(rc.get_raw()))
