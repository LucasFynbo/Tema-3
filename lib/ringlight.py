from neopixel import NeoPixel
from machine import Pin
from time import sleep

class NeoPx: 
    def __init__(self):
        self.pin = Pin(7, Pin.OUT) 
        self.np = NeoPixel(self.pin, 12)

    def on(self):
        for lights in range(0, 12): 
            self.np[lights] = (255, 90, 255)
            self.np.write()

    def off(self):
         for lights in range(0, 12): 
            self.np[lights] = (0, 0, 0)
            self.np.write()


if __name__ == "__main__":
    led = NeoPx()
    while True:
        for lights in range(0, 12):
                led.np[lights - 1] = (0, 0, 0)
                led.np[lights] = (200, 0, 0)
                led.np.write()
                sleep(0.0125)
        
        
        
