import time
import os
from ev3dev.core import *

def num2voice(number):
	number = int(number)
	number_decimal = number / 10
	number_base = number % 10
	NUMBER_CONSTANT = {0:"zero ", 1:"one", 2:"two", 3:"three", 4:"four", 5:"five", 6:"six", 7:"seven",  
                8:"eight", 9:"nine", 10:"ten", 11:"eleven", 12:"twelve", 13:"thirteen",  
                14:"fourteen", 15:"fifteen", 16:"sixteen", 17:"seventeen", 18:"eighteen", 19:"nineteen" };  
	IN_HUNDRED_CONSTANT = {2:"twenty", 3:"thirty", 4:"forty", 5:"fifty", 6:"sixty", 7:"seventy", 8:"eighty", 9:"ninety"} 
	if number_decimal == 0:
		return NUMBER_CONSTANT[str(number_base)]
	else:
		return IN_HUNDRED_CONSTANT[str(number_decimal)] + NUMBER_CONSTANT

time = os.system('date +%H:%M').split(":")
hour = num2voice(time[0])
minute = num2voice(time[1])

Sound.speak("The current time is %s, %s"%(hour, minute))
Sound.play("22d2.wav")
