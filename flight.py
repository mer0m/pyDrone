import pyb, micropython, esc, rc, staccel
micropython.alloc_emergency_exception_buf(100) # to show exception buffer error in console

"""
initialize the controller with:
- a RadioController
- a esc array
- a PID array

Ucons: setpoint array
Usens: sensor array
U: command array
"""
class flight(object):
    def __init__(self):
        self.esc = esc.esc()
        self.rc = rc.rc()
        self.accel = staccel.STAccel()

        self.U = [0]*4
        self.Uc = [0]*4

        self.Kyaw = 0.1
        self.Kpitch = 0.1
        self.Kthrust = 1
        self.Kroll = 0.1
        self.Kx = -100
        self.Ky = 100

    def start(self):
        while True:
            self.Usens = [0, min(100, max(-100, self.accel.y()*self.Ky)), 0, min(100, max(-100, -self.accel.x()*self.Kx))]
            self.Ucons = self.rc.get_raw()    #[yaw, pitch, thrust, roll]

            for i in [0, 1, 2, 3]:
                self.Uc[i] = self.Ucons[i] - self.Usens[i]

	    #TODO real PID
            
            self.U[0] = min(100, max( 0, -self.Kyaw*self.Uc[0] + self.Kpitch*self.Uc[1] + self.Kthrust*self.Uc[2] + self.Kroll*self.Uc[3]))
            self.U[1] = min(100, max( 0,  self.Kyaw*self.Uc[0] + self.Kpitch*self.Uc[1] + self.Kthrust*self.Uc[2] - self.Kroll*self.Uc[3]))
            self.U[2] = min(100, max( 0, -self.Kyaw*self.Uc[0] - self.Kpitch*self.Uc[1] + self.Kthrust*self.Uc[2] - self.Kroll*self.Uc[3]))
            self.U[3] = min(100, max( 0,  self.Kyaw*self.Uc[0] - self.Kpitch*self.Uc[1] + self.Kthrust*self.Uc[2] + self.Kroll*self.Uc[3]))
            
            self.esc.set_pwm_percent(self.U)
            
            pyb.delay(100)
            #pyb.LED(1).toggle()
            #print(Usens, Ucons, U)
            
if __name__=='__main__':
    myUAV = flight()
    myUAV.start()
