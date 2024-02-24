from lib.arducam import Camera          # Arducam driver
from lib.soilsensor import SoilSensor   # SoilSensor driver
from lib.ringlight import NeoPx         # NeoPixel module
from lib.sendimg import ImgFileSender   # Arducam send image module
import threading                        # Threading module

class VerticalFarming:
    def __init__(self):
        self.cam = Camera()
        self.np = NeoPx(pin=7)
        self.soilsensor = SoilSensor()
        self.FileSend = ImgFileSender("/images/image1.jpg", "192.168.99.145", 8000)


if __name__ == "__main__":
    vf = VerticalFarming()