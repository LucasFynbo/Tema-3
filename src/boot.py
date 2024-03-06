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
import Tema_3.lib.wifi as wifi					   # Wifi Connector
import _thread                                 # Threading module
import time

class VerticalFarming:
    def __init__(self):
        self.cam = Camera()
        self.np = NeoPx()
        self.soilsensor = SoilSensor()
        self.FileSend = ImgFileSender("79.171.148.163", 8000)
        ESP_IP = wifi.connect("ITLab", "MaaGodt*7913")
        self.pump = Pump()

        self.np.off()
        self.led_on = 0
    
    def schedule_capture(self, interval):
        _thread.start_new_thread(self.capture_thread,(interval,))

    def capture_thread(self, interval):
        while True:
            currentTime = time.time() # Gets current time
            nextcaptureTime = currentTime + interval # Calculates time until next capture
            remainTime = nextcaptureTime - time.time() # Calculates the remaining time until next capture
            if remainTime > 0: #sleep for the remaining time                    
                time.sleep(remainTime)
                if self.led_on:
                    image_path = self.cam.capture_images()
                else:
                    self.np.on()
                    image_path = self.cam.capture_images()
                    self.np.off()
                print("took picture")
                print(str(image_path))
                self.FileSend.send(image_path)
            else:
                time.sleep(1)
            
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

    def on_pump_if_dry(self, interval):
        while True:
            hum = self.soilsensor.get_hum()
            print(f"Soil moisture: {hum}")
            if hum < 600:
                self.pump.on()
            time.sleep(interval)

if __name__ == "__main__":
    vf = VerticalFarming()
    vf.schedule_capture(60*60*4)
    vf.light_thread(60*60*8)
    vf.pump_thread(60*60)