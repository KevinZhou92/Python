from ev3dev.ev3 import *
from ev3dev.core import *
import time
# MAXIMUM SPEED of LargerMotor = 1050

# initialization
light = Leds()
Sound.speak("Happy to serve you my master! May the force be with you!").wait()
#	Sound.play("22d2.wav")
# light.set_color(light.LEFT, Leds.GREEN)
# light.set_color(light.RIGHT, light.GREEN)
# while True:
	# light.set_color(light.LEFT, Leds.GREEN)
	# head_motor.run_to_rel_pos(position_sp=180, speed_sp=75, stop_action='brake')
	# head_motor.run_to_rel_pos(position_sp=-180, speed_sp=75, stop_action='brake')
	# time.sleep(2)
	# light.set_color(light.LEFT, Leds.RED)
# light.set_color(light.LEFT, Leds.GREEN)
left_motor = LargeMotor('outB')
right_motor = LargeMotor('outA')
left_motor.reset()
right_motor.reset()

rc = RemoteControl()	
light.set_color(light.LEFT, light.RED)
light.set_color(light.RIGHT, light.RED)
light.set_color(light.LEFT, Leds.GREEN)
light.set_color(light.RIGHT, Leds.GREEN)

def left_move(polarity='normal'):
	left_motor.run_forever(speed_sp=1050, polarity=polarity)
	print(left_motor.speed)

def right_move(polarity='normal'):
	right_motor.run_forever(speed_sp=1050, polarity=polarity)
	print(right_motor.speed)

# remote control	
while True:
	# check distance
	#status = dist_available()
	# go forward
	if rc.red_up:
		left_move()
	else:
		left_motor.stop()

	if rc.red_down:
		left_move(polarity='inversed')
	else:
		left_motor.stop()
		
	if rc.blue_up:
		right_move()
	else:
		right_motor.stop()
	
	if rc.blue_down:
		right_move(polarity='inversed')
	else:
		right_motor.stop()
	
	if rc.beacon:
		Sound.play('ready-r2d2.wav').wait()
		

	

