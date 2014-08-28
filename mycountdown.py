import time
import subprocess
import sys
from Tkinter import *
import pygame

class Mycountdown(object):
    
    def __init__(self, work_time, down_time):
        """ Creates a Pomodoro timer.
        
        Parameters:
        work_time : int 
            how much time in minutes you will be working
        down_time : int
            how long in minutes you will be on break"""
            
        self.work_time = work_time * 60
        self.down_time = down_time * 60
        self.done_with_work = time.time()
        self.done_with_break = self.done_with_work 
        
    def start(self):
        """ Start the timer."""
        
        self.start_time = time.time()
        self.done_with_work = self.start_time + self.work_time
        self.done_with_break = self.done_with_work + self.down_time
    
    
    def time_left(self):
        """ return the time left for work in seconds."""
        return self.done_with_work - time.time()
        
    def breaktime_left(self):
        return self.done_with_break - time.time()
        
    def format_time(self, clock_time):
        """ Convert time in seconds to a minute second format.
        
        Parameters:
        clock_time : int
            the time left in seconds. """
        
        minute, sec = divmod(round(clock_time), 60)
        output = "%02d:%02d" % (minute, sec)
        return output
        
    def is_time_expired(self):
        return self.time_left() < 0
        
    def is_breaktime_expired(self):
        return self.breaktime_left() < 0
        
    def play_alert(self):
        
        pygame.init()
        pygame.mixer.init()
        sounda = pygame.mixer.Sound("backupdings.wav")
        
        sounda.play()
        
            
        
        
def no_newline_print(text):
    sys.stdout.write(text)
    # make sure it gets printedS
    sys.stdout.flush()

    
def pomodoro(work_time, down_time):
    """ A countdown timer that alternates between counting down 25 min and 5 min.
	
    Parameters:
    work_time: How many minutes you want to be working.
    down_time: How long you want your break to be in minutes."""
 
    mytimer = Mycountdown(work_time, down_time)
    
    
    mytimer.start()
    while True:
       
        while not mytimer.is_time_expired():
            
            #print the remaining time in minutes
            output = mytimer.format_time(mytimer.time_left())
            no_newline_print(output)
            
            time.sleep(1)
			
            no_newline_print("\x08" * len(output))
            			
		
        print "\n",
        print "Break time!"
        
        mytimer.play_alert()
        #subprocess.call(['powershell', '-c', '(New-Object Media.SoundPlayer "C:\Users\Andrea\mystuff\dings.wav").PlaySync()'])
	
	
        while not mytimer.is_breaktime_expired():
			
           # print the remaining time in minutes
            output = mytimer.format_time(mytimer.breaktime_left())
			
            no_newline_print(output)
			
            time.sleep(1)
            
            no_newline_print("\x08" * len(output))
			
        print "\n",
        print "Work time!"
        mytimer.play_alert()
    
    
pomodoro(0.1, 0.1)
# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
