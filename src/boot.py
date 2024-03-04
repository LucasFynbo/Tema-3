# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import webrepl
#webrepl.start()

from Tema_3.lib.arducam import Camera          # Arducam driver
from Tema_3.lib.soilsensor import SoilSensor   # SoilSensor driver
from Tema_3.lib.ringlight import NeoPx         # NeoPixel module
from Tema_3.lib.sendimg import ImgFileSender   # Arducam send image module
from Tema_3.lib.pump import Pump               # driver for pump
#from Tema_3.lib.wifi import WifiConnector      # Wifi Connector
import _thread                                 # Threading module
import time

class VerticalFarming:
    def __init__(self):
        self.cam = Camera()
        self.np = NeoPx()
        self.soilsensor = SoilSensor()
        self.FileSend = ImgFileSender("192.168.99.145", 8000)
        self.pump = Pump()
        #self.wifi = WifiConnector("ITLAB", "MaaGoddt*7913")
    
    def sendImages(self):
        self.imgFileSender = ImgFileSender() 
    
    def schedule_capture(self, interval):
        _thread.start_new_thread(self.capture_thread,(interval,))

    def wifiConnection(self):
        self.wifi.connect()

    def capture_thread(self, interval):
        while True:
            currentTime = time.time() # Gets current time
            nextcaptureTime = currentTime + interval # Calculates time until next capture
            remainTime = nextcaptureTime - time.time() # Calculates the remaining time until next capture
            if remainTime > 0: #sleep for the remaining time
                time.sleep(remainTime)
                self.cam.capture_images()
                print("took picture")
            else:
                time.sleep(1) # if remaining time == negative, sleep for short time.

    def on_pump_if_dry(self, interval):
        while True:
            hum = self.soilsensor.get_hum()
            print(f"Soil moisture: {hum}")
            if hum < 750:
                self.pump.on()
            time.sleep(interval)
            
    def light_thread(self, interval):
        _thread.start_new_thread(self.manage_light,(interval,))
        
    def pump_thread(self, interval):
        _thread.start_new_thread(self.on_pump_if_dry,(interval,))
        
    def manage_light(self, interval):
        while True:
            vf.np.on()
            time.sleep(interval)
            vf.np.off()
            time.sleep(interval)

if __name__ == "__main__":
    vf = VerticalFarming()
    #vf.wifiConnection()
    vf.schedule_capture(60*60*4)
    vf.light_thread(60*60*8)
    vf.pump_thread(60*10)