from neopixel import NeoPixel
from machine import Pin
from time import sleep

class NeoPx: 
    def __init__(self, pin: int = 0):
        self.pin = Pin(pin, Pin.OUT) 
        self.np = NeoPixel(pin, 12)

    def on(self):
        for lights in range(0, 12): 
            self.np[lights] = (255, 255, 255)
            led.np.write()

    def off(self):
         for lights in range(0, 12): 
            self.np[lights] = (0, 0, 0)
            led.np.write()


if __name__ == "__main__":
    led = NeoPx(pin=7)
    while True:
        for lights in range(0, 12):
                led.np[lights - 1] = (0, 0, 0)
                led.np[lights] = (200, 0, 0)
                led.np.write()
                sleep(0.0125)
        
        
        
