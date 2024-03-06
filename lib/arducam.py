from machine import Pin, SPI, Timer
from time import sleep_ms, ticks_ms, ticks_diff
import os
import json

# modified version of the driver from https://github.com/CoreElectronics/CE-Arducam-MicroPython


class Camera:

# User callable functions
## Main functions
## Setting functions
# Internal functions
## High level internal functions
## Low level

##################### Callable FUNCTIONS #####################

########### CORE PHOTO FUNCTIONS ###########
    def __init__(self, skip_sleep=False, debug_information=False):
        self.CAM_REG_SENSOR_RESET = 0x07
        self.CAM_SENSOR_RESET_ENABLE = 0x40

        ## For get_sensor_config
        self.CAM_REG_SENSOR_ID = 0x40

        self.SENSOR_5MP_1 = 0x81
        self.SENSOR_3MP_1 = 0x82
        self.SENSOR_5MP_2 = 0x83
        self.SENSOR_3MP_2 = 0x84

        ## Camera effect control

        # Set Colour Effect
        self.CAM_REG_COLOR_EFFECT_CONTROL = 0x27

        self.SPECIAL_NORMAL = 0
        self.SPECIAL_COOL = 1
        self.SPECIAL_WARM = 2
        self.SPECIAL_BW = 3
        self.SPECIAL_YELLOWING = 4
        self.SPECIAL_REVERSE = 5
        self.SPECIAL_GREENISH = 6
        self.SPECIAL_LIGHT_YELLOW = 9 # 3MP Only


        # Set Brightness
        self.CAM_REG_BRIGHTNESS_CONTROL = 0X22

        self.BRIGHTNESS_MINUS_4 = 8
        self.BRIGHTNESS_MINUS_3 = 6
        self.BRIGHTNESS_MINUS_2 = 4
        self.BRIGHTNESS_MINUS_1 = 2
        self.BRIGHTNESS_DEFAULT = 0
        self.BRIGHTNESS_PLUS_1 = 1
        self.BRIGHTNESS_PLUS_2 = 3
        self.BRIGHTNESS_PLUS_3 = 5
        self.BRIGHTNESS_PLUS_4 = 7


        # Set Contrast
        self.CAM_REG_CONTRAST_CONTROL = 0X23

        self.CONTRAST_MINUS_3 = 6
        self.CONTRAST_MINUS_2 = 4
        self.CONTRAST_MINUS_1 = 2
        self.CONTRAST_DEFAULT = 0
        self.CONTRAST_PLUS_1 = 1
        self.CONTRAST_PLUS_2 = 3
        self.CONTRAST_PLUS_3 = 5


        # Set Saturation
        self.CAM_REG_SATURATION_CONTROL = 0X24

        self.SATURATION_MINUS_3 = 6
        self.SATURATION_MINUS_2 = 4
        self.SATURATION_MINUS_1 = 2
        self.SATURATION_DEFAULT = 0
        self.SATURATION_PLUS_1 = 1
        self.SATURATION_PLUS_2 = 3
        self.SATURATION_PLUS_3 = 5


        # Set Exposure Value
        self.CAM_REG_EXPOSURE_CONTROL = 0X25

        self.EXPOSURE_MINUS_3 = 6
        self.EXPOSURE_MINUS_2 = 4
        self.EXPOSURE_MINUS_1 = 2
        self.EXPOSURE_DEFAULT = 0
        self.EXPOSURE_PLUS_1 = 1
        self.EXPOSURE_PLUS_2 = 3
        self.EXPOSURE_PLUS_3 = 5


        # Set Whitebalance
        self.CAM_REG_WB_MODE_CONTROL = 0X26

        self.WB_MODE_AUTO = 0
        self.WB_MODE_SUNNY = 1
        self.WB_MODE_OFFICE = 2
        self.WB_MODE_CLOUDY = 3
        self.WB_MODE_HOME = 4

        # Set Sharpness
        self.CAM_REG_SHARPNESS_CONTROL = 0X28 #3MP only

        self.SHARPNESS_NORMAL = 0
        self.SHARPNESS_1 = 1
        self.SHARPNESS_2 = 2
        self.SHARPNESS_3 = 3
        self.SHARPNESS_4 = 4
        self.SHARPNESS_5 = 5
        self.SHARPNESS_6 = 6
        self.SHARPNESS_7 = 7
        self.SHARPNESS_8 = 8

        # Set Autofocus
        self.CAM_REG_AUTO_FOCUS_CONTROL = 0X29 #5MP only

        # Set Image quality
        self.CAM_REG_IMAGE_QUALITY = 0x2A

        self.IMAGE_QUALITY_HIGH = 0
        self.IMAGE_QUALITY_MEDI = 1
        self.IMAGE_QUALITY_LOW = 2

        # Manual gain, and exposure are explored in the datasheet - https://www.arducam.com/downloads/datasheet/Arducam_MEGA_SPI_Camera_Application_Note.pdf

        # Device addressing
        self.CAM_REG_DEBUG_DEVICE_ADDRESS = 0x0A
        self.deviceAddress = 0x78

        # For Waiting
        self.CAM_REG_SENSOR_STATE = 0x44
        self.CAM_REG_SENSOR_STATE_IDLE = 0x01

        # Setup for capturing photos
        self.CAM_REG_FORMAT = 0x20

        self.CAM_IMAGE_PIX_FMT_JPG = 0x01
        self.CAM_IMAGE_PIX_FMT_RGB565 = 0x02
        self.CAM_IMAGE_PIX_FMT_YUV = 0x03

        # Resolution settings
        self.CAM_REG_CAPTURE_RESOLUTION = 0x21

        # Some resolutions are not available - refer to datasheet https://www.arducam.com/downloads/datasheet/Arducam_MEGA_SPI_Camera_Application_Note.pdf
        #     RESOLUTION_160X120 = 0X00
        self.RESOLUTION_320X240 = 0X01
        self.RESOLUTION_640X480 = 0X02
        #     RESOLUTION_800X600 = 0X03
        self.RESOLUTION_1280X720 = 0X04
        #     RESOLUTION_1280X960 = 0X05
        self.RESOLUTION_1600X1200 = 0X06
        self.RESOLUTION_1920X1080 = 0X07
        self.RESOLUTION_2048X1536 = 0X08 # 3MP only
        self.RESOLUTION_2592X1944 = 0X09 # 5MP only
        self.RESOLUTION_96X96 = 0X0a
        self.RESOLUTION_128X128 = 0X0b
        self.RESOLUTION_320X320 = 0X0c

        self.valid_3mp_resolutions = {
            '320x240': self.RESOLUTION_320X240, 
            '640x480': self.RESOLUTION_640X480, 
            '1280x720': self.RESOLUTION_1280X720, 
            '1600x1200': self.RESOLUTION_1600X1200,
            '1920x1080': self.RESOLUTION_1920X1080,
            '2048x1536': self.RESOLUTION_2048X1536,
            '96x96': self.RESOLUTION_96X96,
            '128x128': self.RESOLUTION_128X128,
            '320x320': self.RESOLUTION_320X320
        }

        self.valid_5mp_resolutions = {
            '320x240': self.RESOLUTION_320X240, 
            '640x480': self.RESOLUTION_640X480, 
            '1280x720': self.RESOLUTION_1280X720, 
            '1600x1200': self.RESOLUTION_1600X1200,
            '1920x1080': self.RESOLUTION_1920X1080,
            '2592x1944': self.RESOLUTION_2592X1944,
            '96x96': self.RESOLUTION_96X96,
            '128x128': self.RESOLUTION_128X128,
            '320x320': self.RESOLUTION_320X320
        }

        # FIFO and State setting registers
        self.ARDUCHIP_FIFO = 0x04
        self.FIFO_CLEAR_ID_MASK = 0x01
        self.FIFO_START_MASK = 0x02

        self.ARDUCHIP_TRIG = 0x44
        self.CAP_DONE_MASK = 0x04

        self.FIFO_SIZE1 = 0x45
        self.FIFO_SIZE2 = 0x46
        self.FIFO_SIZE3 = 0x47

        self.SINGLE_FIFO_READ = 0x3D
        self.BURST_FIFO_READ = 0X3C

        # Size of image_buffer (Burst reading)
        self.BUFFER_MAX_LENGTH = 590 # There seems to be an arbitrary maximum of 590 on this

        # For 5MP startup routine
        self.WHITE_BALANCE_WAIT_TIME_MS = 500
		
        self.spi_bus = SPI(1, baudrate=8000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(36), mosi=Pin(35), miso=Pin(37))
        self.cs = Pin(34, Pin.OUT, value=1)
        self.camera_idx = "3MP"

        self._write_reg(self.CAM_REG_SENSOR_RESET, self.CAM_SENSOR_RESET_ENABLE) # Reset camera
        self._wait_idle()
        self._get_sensor_config() # Get camera sensor information
        self._wait_idle()
        self._write_reg(self.CAM_REG_DEBUG_DEVICE_ADDRESS, self.deviceAddress)
        self._wait_idle()


        self.run_start_up_config = True

		# Set default format and resolution
        self.current_pixel_format = self.CAM_IMAGE_PIX_FMT_JPG
        self.old_pixel_format = self.current_pixel_format
		
        self.current_resolution_setting = self.RESOLUTION_640X480 # ArduCam driver defines this as mode
        self.old_resolution = self.current_resolution_setting
		
        self.set_filter(self.SPECIAL_NORMAL)
		
        self.received_length = 0
        self.total_length = 0
		
		# Burst setup
        self.first_burst_run = False
        self.image_buffer = bytearray(self.BUFFER_MAX_LENGTH)
        self.valid_image_buffer = 0
				
		# Tracks the AWB warmup time
        self.start_time = ticks_ms()
        if debug_information:
            print('Camera version =', self.camera_idx)
        if self.camera_idx == '3MP':
            self.startup_routine_3MP()
		
        if self.camera_idx == '5MP' and skip_sleep == False:
            sleep_ms(self.WHITE_BALANCE_WAIT_TIME_MS)

    def startup_routine_3MP(self):
		# Leave the shutter open for some time seconds (i.e. take a few photos without saving)
        print('Running 3MP startup routine')
        self.capture_jpg()
        self.saveJPG('dummy_image.jpg')
        os.remove('dummy_image.jpg')
        print('Startup routine complete')

    '''
	Issue warning if the filepath doesnt end in .jpg (Blank) and append
	Issue error if the filetype is NOT .jpg
	'''
    def capture_jpg(self):
        if (ticks_diff(ticks_ms(), self.start_time) <= self.WHITE_BALANCE_WAIT_TIME_MS) and self.camera_idx == '5MP':
            print('Please add a ', self.WHITE_BALANCE_WAIT_TIME_MS, 'ms delay to allow for white balance to run')
			
        else:
	        #print('Starting capture JPG')
			# JPG, bmp ect
			# TODO: PROPERTIES TO CONFIGURE THE PIXEL FORMAT
            if (self.old_pixel_format != self.current_pixel_format) or self.run_start_up_config:
                self.old_pixel_format = self.current_pixel_format
                self._write_reg(self.CAM_REG_FORMAT, self.current_pixel_format) # Set to capture a jpg
                self._wait_idle()
	            #print('old',self.old_resolution,'new',self.current_resolution_setting)
				# TODO: PROPERTIES TO CONFIGURE THE RESOLUTION
            if (self.old_resolution != self.current_resolution_setting) or self.run_start_up_config:
                self.old_resolution = self.current_resolution_setting
                self._write_reg(self.CAM_REG_CAPTURE_RESOLUTION, self.current_resolution_setting)
	            #print('setting res', self.current_resolution_setting)
                self._wait_idle()
			
            self.run_start_up_config = False
			
			# Start capturing the photo
            self._set_capture()

    def saveJPG(self, filename):
        imagefile = open(filename,'ab')
        endmarker_recieved = False
        startmarker_recieved = False
        startmarker = b'\xff\xd8'
        endmarker = b'\xff\xd9'
        last_byte = 0x00
		
        while not endmarker_recieved:
            self.cs.value(0)
            self.spi_bus.readinto(self.image_buffer, self.BURST_FIFO_READ)
            self.cs.value(1)
			
            self.image_buffer[0] = last_byte
            last_byte = self.image_buffer[-1]
			
            if startmarker in self.image_buffer:
                startmarker_recieved = True
                startmarker_index = self.image_buffer.find(startmarker)
				#print("header found" + str(startmarker_index))
                imagefile.write(self.image_buffer[startmarker_index:])
			
            if endmarker in self.image_buffer:
                endmarker_recieved = True
                endmarker_index = self.image_buffer.find(endmarker)
				#print("end found" + str(endmarker_index))
                imagefile.write(self.image_buffer[1:endmarker_index+2])
			
            if startmarker_recieved and not endmarker_recieved:
                imagefile.write(self.image_buffer[1:])
			
        imagefile.close()
		

    @property
    def resolution(self):
        return self.current_resolution_setting
    @resolution.setter
    def resolution(self, new_resolution):
        input_string_lower = new_resolution.lower()        
        if self.camera_idx == '3MP':
            if input_string_lower in self.valid_3mp_resolutions:
                self.current_resolution_setting = self.valid_3mp_resolutions[input_string_lower]
            else:
                raise ValueError("Invalid resolution provided for {}, please select from {}".format(self.camera_idx, list(self.valid_3mp_resolutions.keys())))

        elif self.camera_idx == '5MP':
            if input_string_lower in self.valid_5mp_resolutions:
                self.current_resolution_setting = self.valid_5mp_resolutions[input_string_lower]
            else:
                raise ValueError("Invalid resolution provided for {}, please select from {}".format(self.camera_idx, list(self.valid_5mp_resolutions.keys())))

    def set_pixel_format(self, new_pixel_format):
        self.current_pixel_format = new_pixel_format

########### ACCSESSORY FUNCTIONS ###########

    # TODO: Complete for other camera settings
    # Make these setters - https://github.com/CoreElectronics/CE-PiicoDev-Accelerometer-LIS3DH-MicroPython-Module/blob/abcb4337020434af010f2325b061e694b808316d/PiicoDev_LIS3DH.py#L118C1-L118C1

    def set_brightness_level(self, brightness):
        self._write_reg(self.CAM_REG_BRIGHTNESS_CONTROL, brightness)
        self._wait_idle()

    def set_filter(self, effect):
        self._write_reg(self.CAM_REG_COLOR_EFFECT_CONTROL, effect)
        self._wait_idle()

    def set_saturation_control(self, saturation_value):
        self._write_reg(self.CAM_REG_SATURATION_CONTROL, saturation_value)
        self._wait_idle()

    def set_exposure(self, exposure):
        self._write_reg(self.CAM_REG_EXPOSURE_CONTROL, exposure)
        self._wait_idle()

    def set_contrast(self, contrast):
        self._write_reg(self.CAM_REG_CONTRAST_CONTROL, contrast)
        self._wait_idle()

    def set_white_balance(self, environment):
        register_value = self.WB_MODE_AUTO

        if environment == 'sunny':
            register_value = self.WB_MODE_SUNNY
        elif environment == 'office':
            register_value = self.WB_MODE_OFFICE
        elif environment == 'cloudy':
            register_value = self.WB_MODE_CLOUDY
        elif environment == 'home':
            register_value = self.WB_MODE_HOME
        elif self.camera_idx == '3MP':
            print('TODO UPDATE: For best results set a White Balance setting')

        self.white_balance_mode = register_value
        self._write_reg(self.CAM_REG_WB_MODE_CONTROL, register_value)
        self._wait_idle()


##################### INTERNAL FUNCTIONS - HIGH LEVEL #####################

########### CORE PHOTO FUNCTIONS ###########
    def _clear_fifo_flag(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_CLEAR_ID_MASK)

    def _start_capture(self):
        self._write_reg(self.ARDUCHIP_FIFO, self.FIFO_START_MASK)

    def _set_capture(self):
        self._clear_fifo_flag()
        self._wait_idle()
        self._start_capture()
        while (self._get_bit(self.ARDUCHIP_TRIG, self.CAP_DONE_MASK) == 0):
            sleep_ms(1)
        self.received_length = self._read_fifo_length()
        self.total_length = self.received_length
        self.burst_first_flag = False
    
    def _read_fifo_length(self): # TODO: CONFIRM AND SWAP TO A 3 BYTE READ
        len1 = int.from_bytes(self._read_reg(self.FIFO_SIZE1),1)
        len2 = int.from_bytes(self._read_reg(self.FIFO_SIZE2),1)
        len3 = int.from_bytes(self._read_reg(self.FIFO_SIZE3),1)
        length = ((len3 << 16) | (len2 << 8) | len1) & 0xffffff
		#print(len1,len2,len3,length)
        return length

    def _get_sensor_config(self):
        camera_idx = self._read_reg(self.CAM_REG_SENSOR_ID);
        self._wait_idle()
        if (int.from_bytes(camera_idx, 1) == self.SENSOR_3MP_1) or (int.from_bytes(camera_idx, 1) == self.SENSOR_3MP_2):
            self.camera_idx = '3MP'
        if (int.from_bytes(camera_idx, 1) == self.SENSOR_5MP_1) or (int.from_bytes(camera_idx, 1) == self.SENSOR_5MP_2):
            self.camera_idx = '5MP'


##################### INTERNAL FUNCTIONS - LOW LEVEL #####################

    def _bus_write(self, addr, val):
        self.cs.value(0)
        self.spi_bus.write(bytes([addr]))
        self.spi_bus.write(bytes([val])) # FixMe only works with single bytes
        self.cs.value(1)
        sleep_ms(1) # From the Arducam Library
        return 1
    
    def _bus_read(self, addr):
        self.cs.value(0)
        self.spi_bus.write(bytes([addr]))
        data = self.spi_bus.read(1) # Only read second set of data
        data = self.spi_bus.read(1)
        self.cs.value(1)
        return data

    def _write_reg(self, addr, val):
        self._bus_write(addr | 0x80, val)

    def _read_reg(self, addr):
        data = self._bus_read(addr & 0x7F)
        return data # TODO: Check that this should return raw bytes or int (int.from_bytes(data, 1))
    
    def _wait_idle(self):
        data = self._read_reg(self.CAM_REG_SENSOR_STATE)
        while ((int.from_bytes(data, 1) & 0x03) == self.CAM_REG_SENSOR_STATE_IDLE):
            data = self._read_reg(self.CAM_REG_SENSOR_STATE)
            sleep_ms(2)

    def _get_bit(self, addr, bit):
        data = self._read_reg(addr)
        return int.from_bytes(data, 1) & bit

    def capture_images(self):
        self.resolution = '320x240'
		#cam.resolution = '640x480'
        self.set_brightness_level(self.BRIGHTNESS_PLUS_4)
        self.set_contrast(self.CONTRAST_MINUS_3)
        self.set_filter(self.SPECIAL_NORMAL)
        t = 0
			
        existing_files = os.listdir("images")
        existing_numbers = [int(file.split('.')[0].split('image')[1]) for file in existing_files if file.startswith("image")]
        max_existing_number = max(existing_numbers) if existing_numbers else -0
			
		# Capture 1 more image without overwriting existing ones
        image_number = max_existing_number + 1 if max_existing_number != -1 else 0
        image_path = f'images/image{image_number}.jpg'
        self.capture_jpg()
        t1 = ticks_ms()
        self.saveJPG(image_path)
		
			
        t += ticks_ms()-t1
        print("Total time:" + str(t))
        return image_path
    
if __name__ == "__main__":
    cam = Camera()
    print("Finished cam")
    cam.capture_images()

