import RPi.GPIO as GPIO
import time
import subprocess



def check_internet():
	"""
	Function to check the internet connection by pinging the address.
	Returns true if the internet is connected , otherwise False.
	"""
	try: 
		subprocess.check_output(['ping', '-c', '1', '192.168.200.1'])
		return True
	except subprocess.CalledProcessError:
		return False

def main():
	# setup GPIO
	relay_pin = 17 # GPIO pin that gives 3.3v Output pin 1 and 17 work
	print("setup Complete")

	# Initialize variables
	no_internet_counter = 0
	recently_open_counter = 0
	last_open_time = int(time.time())
	last_reset_time = int(time.time())
	current_time = None
	try:
		while True:
			current_time = int(time.time())
			print(current_time)
			# Reset the count every 2 hrs
			if ((current_time - last_reset_time) >= (2 * 60 * 60)):
				no_internet_counter = 0
				print("2hr counter")
				last_reset_time = current_time
			
			# Check internet connection every minute
			if ((current_time - last_reset_time) >= 60):
				if not check_internet():
					no_internet_counter += 1
					print("Internet check")
					if no_internet_counter <= 3:
						print("Internet connection lost. Opening relay...")
						GPIO.setmode(GPIO.BCM)
						GPIO.setup(relay_pin, GPIO.OUT) # open the relay
						last_open_time = current_time
						time.sleep(15) # Wait 15 seconds
						print("closing relay...")
						GPIO.cleanup() # Closing the relay
						time.sleep(15*60)
			else:
				recently_open_counter = 0
				no_internet_counter = 0
	except KeyboardInterrupt:
		# cleanup GPIO on exit
		GPIO.cleanup()

if __name__ == '__main__':
	# import sys
	# sys.exit(main(sys.argv))
	main()
