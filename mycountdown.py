import time
import subprocess
import sys
from Tkinter import *

def pomodoro(work_time, down_time):
	""" A countdown timer that alternates between counting down 25 min and 5 min.
	
	Parameters:
	work_time: How many minutes you want to be working.
	down_time: How long you want your break to be in minutes."""
	# work_time and down_time are converted to seconds.
	work_time = work_time * 60
	down_time = down_time * 60

	no_newline_print = sys.stdout.write
	
	while True:
	
		donewithwork = time.time() + work_time
		# The very first time no_newline_print runs we need we will not have printed output yet so having output be an empty string keeps
		# the cursor at the beginning of the line. 
		output = ""
		while time.time() < donewithwork:
			
			minute, sec = divmod(round(donewithwork - time.time()), 60)
			
			no_newline_print("\x08" * len(output))
			output = "%02d:%02d" % (minute, sec)
			
			#print the remaining time in minutes
			sys.stdout.write(output)
			# make sure it gets written to the screen
			sys.stdout.flush()
			
			time.sleep(1)
		
		print "\n",
		print "Break time!"
	
		subprocess.call(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\Users\Andrea\mystuff\dings.wav").PlaySync()'])
	
	
		donewithbreak = donewithwork + down_time
		output = ""
		while time.time() < donewithbreak:
			
			minute, sec = divmod(round(donewithbreak - time.time()), 60)
			
			no_newline_print("\x08" * len(output))
			output = "%02d:%02d" % (minute, sec)
			
			sys.stdout.write(output)
			
			sys.stdout.flush()
			
			time.sleep(1)
			
		print "\n",
		print "Work time!"
		subprocess.call(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\Users\Andrea\mystuff\dings.wav").PlaySync()'])
		
		
pomodoro(25,5)
# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
	
