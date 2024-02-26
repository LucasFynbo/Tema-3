from neopixel import NeoPixel
from machine import Pin
from time import sleep
#mængde af lyx artikle: https://backyardgardenersnetwork.org/lettuce-light-requirements/
class NeoPx: 
    def __init__(self):
        self.pin = Pin(7, Pin.OUT) 
        self.np = NeoPixel(self.pin, 12)

    def on(self):
        for lights in range(0, 12): 
            self.np[lights] = (255, 255, 255)
            self.np.write()

    def off(self):
         for lights in range(0, 12): 
            self.np[lights] = (0, 0, 0)
            self.np.write()
            
    def setSchedule(self, NeoPx):
        while True:
            NeoPx.off()
            sleep(43200)
            NeoPx.on()
            sleep(43200)


if __name__ == "__main__":
    led = NeoPx()
    
    led.on()
    
    led.setSchedule(led)
    
        
        
        
