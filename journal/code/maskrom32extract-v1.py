# Assume 1mb MaskROM
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

counter_clock = 19
counter_clear = 26
mask_oe = 6
mask_cs = 13
snes_d0 = 18
snes_d1 = 23
snes_d2 = 24
snes_d3 = 25
snes_d4 = 12
snes_d5 = 16
snes_d6 = 20
snes_d7 = 21

outputs = [counter_clock, counter_clear, mask_oe, mask_cs]
datapins = [18,23,24,25,12,16,20,21]

for i in datapins:
	GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for i in outputs:
	GPIO.setup(i, GPIO.OUT)

def cycle(states, pins, delay):
	for s in states:
		for p in pins:
			GPIO.output(p, s)
		time.sleep(delay)

# Make sure the cartridge and counters are reset
GPIO.output(counter_clock, False)
cycle([True, False], [counter_clear], 1)

a = 0

result = open("rom.sfc", "wb")

while True:

	# Some sort of progress
	if (a&1023)==0:
		print(a)

	# Perform snes read
	# http://www.cs.umb.edu/~bazz/snes/cartridges/electronics/speeds.html
	GPIO.output(mask_oe, True)
	GPIO.output(mask_cs, True)
	GPIO.output(counter_clock, False)

	# Adress line already setup

	GPIO.output(mask_oe, False)
	GPIO.output(mask_cs, False)

	# Wait for data to appear
	# Python is so slow so no need to wait!

	b = 0
	for d in range(8):
		s = GPIO.input(datapins[d])
		b = b + (s<<d)

	result.write("%c" % (b))

	# Last supported byte?
	if a==(1<<20):
		break

	GPIO.output(mask_oe, True)
	GPIO.output(mask_cs, True)
	GPIO.output(counter_clock, True) # Advance to next adr
	a = a + 1

	# Sleep to make counter advance. Python slow!