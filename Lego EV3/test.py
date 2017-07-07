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
left_motor = LargeMotor('outA')
right_motor = LargeMotor('outB')
left_motor.reset()
right_motor.reset()

#rc = RemoteControl()	
light.set_color(light.LEFT, light.RED)
light.set_color(light.RIGHT, light.RED)
light.set_color(light.LEFT, Leds.GREEN)
light.set_color(light.RIGHT, Leds.GREEN)

def dist_available():
	distance_sensor = InfraredSensor('in1', mode='IR-PROX')
	print(distance_sensor.proximity)
	if distance_sensor.proximity < 75:
		Sound.play('fuck-r2d2.wav').wait()
		return 0
	else : 
		return 1
	
def move_forward(stop_action='coast'):
	left_motor.run_timed(stop_action=stop_action, speed_sp = 1050, time_sp = 1000)
	right_motor.run_timed(stop_action=stop_action, speed_sp = 1050, time_sp = 1000)

def move_backward(time_sp, stop_action='coast'):
	left_motor.run_timed(time_sp=time_sp, speed_sp = 1050, polarity = 'inversed')
	right_motor.run_timed(time_sp=time_sp, speed_sp = 1050, polarity = 'inversed')
	
def turn_left(time_sp, polarity='normal', stop_action='brake'):
	print('turn left %s'%(left_motor.polarity))
	left_motor.polarity = polarity
	left_motor.run_timed(polarity=polarity, speed_sp = 1050, time_sp = time_sp, stop_action = stop_action)
	while 'running' in left_motor.state:
		continue

def turn_right(time_sp, polarity='normal', stop_action='brake'):
	print('turn right %s'%(right_motor.polarity))
	right_motor.polarity = polarity
	right_motor.run_timed(polarity=polarity, speed_sp = 1050, time_sp = time_sp, stop_action = stop_action)
	while 'running' in right_motor.state:
		continue
		
def turn_opposite():
	print('turn opposite')
	turn_left(time_sp=2450, stop_action='brake')
	while 'running' in left_motor.state:
		continue

def discover():	
	turn_left(time_sp=1200)
	left_available = dist_available()
	turn_left(time_sp=1200, polarity='inversed')

	turn_right(time_sp=1200)
	right_available = dist_available()
	turn_right(time_sp=1200, polarity='inversed')
	
	turn_opposite()
	back_available = dist_available()
	turn_opposite()

	if left_available:
		turn_left(time_sp=1200)
	elif right_available:
		turn_right(time_sp=1200)
	elif back_available:
		turn_left(time_sp=2450, stop_action='brake')
	
	left_motor.reset()
	right_motor.reset()
	
# autonomous
while True:
	if dist_available():
		move_forward()
	else:
		discover()
		
	# prevent from being stuck at the wall
	
	

# remote control	
while True:
	break
	# check distance
	#status = dist_available()
	
	# go forward
	while rc.red_up and rc.blue_up:
		move_forward(stop_action='brake')
			
	# go backward
	while rc.red_down and rc.blue_down:
		move_backward(stop_action='brake')
	
	# turn left	
	while rc.red_up and not rc.blue_down:
		turn_left()
		
	# turn left2	
	while rc.blue_down and not rc.red_down:
		turn_left(polarity='inversed',)
	
	# turn right	
	while rc.blue_up and not rc.red_down:
		turn_right()
	
	# turn right2	
	while rc.red_down and not rc.blue_down:
		turn_right(polarity = 'inversed')
	
	if rc.beacon:
		Sound.speak('ready-r2d2.wav').wait()
		
	left_motor.reset()
	right_motor.reset()
	

