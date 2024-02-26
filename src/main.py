from Tema_3.lib.arducam import Camera          # Arducam driver
from Tema_3.lib.soilsensor import SoilSensor   # SoilSensor driver
from Tema_3.lib.ringlight import NeoPx         # NeoPixel module
from Tema_3.lib.sendimg import ImgFileSender   # Arducam send image module
from Tema_3.lib.pump import Pump               # driver for pump
import _thread                        # Threading module
import time


class VerticalFarming:
    def __init__(self):
        self.cam = Camera()
        self.np = NeoPx()
        self.soilsensor = SoilSensor()
        self.FileSend = ImgFileSender("192.168.99.145", 8000)
        self.pump = Pump()
    
    def sendImages(self):
        self.imgFileSender = ImgFileSender() 
    
    def schedule_capture(self, interval,):
        _thread.start_new_thread(self.capture_thread, (interval,))
        

    def capture_thread(self, interval):
        while True:
            currentTime = time.time() # Gets current time
            nextcaptureTime = currentTime + interval # Calculates time until next capture
            remainTime = nextcaptureTime - time.time() # Calculates the remaining time until next capture
            if remainTime > 0: #sleep for the remaining time
                time.sleep(remainTime)
            else:
                time.sleep(1) # if remaining time == negative, sleep for short time.

    def on_pump_if_dry(self):
        hum = self.soilsensor.get_hum()
        self.pump.on()
        


if __name__ == "__main__":
    vf = VerticalFarming()
    soilsensor = SoilSensor()
    vf.schedule_capture(24 * 60 * 60)
    while True:
        hum = soilsensor.get_hum()
        print(f"Soil moisture: {hum}")
        vf.on_pump_if_dry()
        vf.np.on()
        time.sleep(1)
