from machine import Pin, PWM
from time import sleep

class Pump:
    def __init__(self):
        self.pin= Pin(6, Pin.OUT)
        self.pwm =PWM(self.pin, freq=200, duty_u16=0)

    def duty(self,procent):
        self.pwm.duty_u16(int(65535/100*procent))
        
if __name__ == "__main__":
    p = Pump()
    while True:
        p.duty(100)
        sleep(6)
        p.duty(0)
        sleep(20)