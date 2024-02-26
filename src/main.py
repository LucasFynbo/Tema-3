from tema_3.lib.arducam import Camera          # Arducam driver
from tema_3lib.soilsensor import SoilSensor   # SoilSensor driver
from tema_3.lib.ringlight import NeoPx         # NeoPixel module
from tema_3.lib.sendimg import ImgFileSender   # Arducam send image module
import _thread                        # Threading module
import time


class VerticalFarming:
    def __init__(self):
        self.cam = Camera()
        self.np = NeoPx(pin=7)
        self.soilsensor = SoilSensor()
        self.FileSend = ImgFileSender("/images/image1.jpg", "192.168.99.145", 8000)
    
    def sendImages(self):
        self.imgFileSender = ImgFileSender() 
    
    def schedule_capture(self, interval,):
        _thread.start_new_thread(self.capture_thread, (interval,))
        
    def capture_thread(self, interval):
        while True:
            currentTime = time.time() # Gets current time
            nextcaptureTime = currentTime + interval # Calculates time until next capture
            self.captureAndsendImages() # Captures and sends images
            remainTime = nextcaptureTime - time.time() # Calculates the remaining time until next capture
            if remainTime > 0: #sleep for the remaining time
                time.sleep(remainTime)
            else:
                time.sleep(1) # if remaining time == negative, sleep for short time.


if __name__ == "__main__":
    vf = VerticalFarming()
    soilsensor = SoilSensor()
    vf.schedule_capture(24 * 60 * 60)
    while True:
        hum = soilsensor.get_hum()
        print(f"Soil moisture: {hum}")
        time.sleep(1)
