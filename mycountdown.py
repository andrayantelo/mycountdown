import time
import subprocess
import sys

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
		start_time = time.time()
		finish_time = start_time + work_time
	
		while time.time() < finish_time:
			
			minute, sec = divmod(round(finish_time - time.time()), 60)
			output = "%d:%02d" % (minute, sec)
			
			no_newline_print("\x08" * len(output))
		#print the remaining time in minutes
			sys.stdout.write(output)
		# make sure it gets written to the screen
			sys.stdout.flush()
			
			time.sleep(1)
		
		print "\n",
		print "Break time!"
	
		subprocess.call(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\Users\Andrea\mystuff\dings.wav").PlaySync()'])
	
	
		break_finish = finish_time + down_time	
		while time.time() < break_finish:
			
			minute, sec = divmod(round(break_finish - time.time()), 60)
			
			no_newline_print("\x08" * len(output))
			
			sys.stdout.write(output)
			
			sys.stdout.flush()
			
			time.sleep(1)
			
		print "\n",
		print "Work time!"
		subprocess.call(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\Users\Andrea\mystuff\dings.wav").PlaySync()'])
		
		
	
# want to figure out a way to pause it
# make a UI
#
	
