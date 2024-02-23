from machine import Pin, I2C
from time import sleep_ms

class SoilSensor:

	# Registers:
	# https://learn.adafruit.com/adafruit-seesaw-atsamd09-breakout/reading-and-writing-data
	SEESAW_STATUS_BASE = 0x00
	SEESAW_STATUS_TEMP = 0x04

	SEESAW_TOUCH_BASE = 0x0F
	SEESAW_TOUCH_CHANNEL_OFFSET = 0x10

	SEESAW_GPIO_BASE = 0x01
	SEESAW_GPIO_DIRSET_BULK = 0x02
	SEESAW_GPIO_DIRCLR_BULK = 0x03
	SEESAW_GPIO_BULK = 0x04
	SEESAW_GPIO_BULK_SET = 0x05
	SEESAW_GPIO_BULK_CLR = 0x06
	SEESAW_GPIO_BULK_TOGGLE = 0x07
	#SEESAW_GPIO_DIRSET_BULK  # this->write(SEESAW_GPIO_BASE, SEESAW_GPIO_DIRSET_BULK, cmd, 4);
	
	def __init__(self, i2c_bus, address=0x36):
		self.bus = i2c_bus
		self.addr = address
		self.led_pin = (1<<27).to_bytes(4, 'big')
		if address not in i2c_bus.scan():
			print("Soilmoisture sensor not found!")
		self.temp_cmd = bytes([self.SEESAW_STATUS_BASE, self.SEESAW_STATUS_TEMP])
		self.hum_cmd = bytes([self.SEESAW_TOUCH_BASE, self.SEESAW_TOUCH_CHANNEL_OFFSET])
		
		self.bus.writeto(self.addr, bytes([self.SEESAW_GPIO_BASE, self.SEESAW_GPIO_DIRCLR_BULK])+self.led_pin)

	def set_led(self, state): # TODO: Doesnt seem to work
		cmd = bytes([self.SEESAW_GPIO_BASE, self.SEESAW_GPIO_BULK_SET if state else self.SEESAW_GPIO_BULK_CLR])+self.led_pin
		self.bus.writeto(self.addr, cmd)

	def get_temp(self):
		self.bus.writeto(self.addr, self.temp_cmd)
		sleep_ms(1)
		result = self.bus.readfrom(self.addr, 4)
		return 0.0000152587890625 * int.from_bytes(result, 'big') # 0.0000152587890625 = 1/(2^16)

	# 200 (very dry) to 2000 (very wet)
	def get_hum(self):
		self.bus.writeto(self.addr, self.hum_cmd)
		sleep_ms(4) # Delay to allow sample to complete
		result = self.bus.readfrom(self.addr, 2)
		return int.from_bytes(result, 'big')


if __name__ == "__main__":
	sens = SoilSensor(I2C(1, scl=Pin(9), sda=Pin(8)))
	while True:
		t=0
		#t = sens.get_temp()
		h = sens.get_hum()
		print(f"Temp, {t}, Hum, {h}")
		sleep_ms(500)