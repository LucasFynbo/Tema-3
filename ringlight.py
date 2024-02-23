from neopixel import NeoPixel
from machine import Pin
from time import sleep
pin = Pin(7, Pin.OUT) # set GPIO0 to output to drive NeoPixels 
np = NeoPixel(pin, 12) # create NeoPixel driver on GPIO0 for 8 pixels 
 

while True:
    for lights in range(0, 12):
        np[lights - 1] = (0, 0, 0) # set the first pixel to white
        np[lights] = (200, 0, 0) # set the first pixel to white
        np.write() # write data to all pixels
        sleep(0.0125)
        
        
