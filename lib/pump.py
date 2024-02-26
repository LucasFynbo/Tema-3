from machine import Pin, PWM
from time import sleep

class Pump:
    def __init__(self):
        self.pin= Pin(6, Pin.OUT)
        self.pwm =PWM(self.pin, freq=200, duty_u16=0)

    def on(self):
        self.pwm.duty_u16(65535)
        sleep(6)
        self.pwm.duty_u16(0)
        
if __name__ == "__main__":
    p = Pump()
    p.on()