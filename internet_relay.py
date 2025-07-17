#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  internet_relay.py
#  
#  Copyright 2024  <tech@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import RPi.GPIO as GPIO
import time
import subprocess



def check_internet():
	"""
	Function to check the internet connection by pinging the address.
	Returns true if the internet is connected , otherwise False.
	"""
	try: 
		subprocess.check_output(['ping', '-c', '1', 'google.com'])
		return True
	except subprocess.CalledProcessError:
		return False

def main():
	# setup GPIO
	relay_pin = 17 # GPIO pin that gives 3.3v Output pin 1 and 17 work
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(relay_pin, GPIO.OUT)
	print("setup Complete")

	# Initialize variables
	no_internet_counter = 0
	recently_open_counter = 0
	last_open_time = int(time.time())
	last_reset_time = int(time.time())
	current_time = None
	try:
		while True:
			print("pin off")
			GPIO.cleanup()
			time.sleep(1)
			print("pin on")
			GPIO.setmode(GPIO.BCM)
			GPIO.setup(relay_pin, GPIO.OUT)
			time.sleep(1)
			
	except KeyboardInterrupt:
		# cleanup GPIO on exit
		GPIO.cleanup()

if __name__ == '__main__':
	# import sys
	# sys.exit(main(sys.argv))
	main()
