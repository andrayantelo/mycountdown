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
       
        
    def start(self, done_time):
        """ Start the timer."""
        
        self.start_time = time.time()
        self.done_with_work = self.start_time + done_time
        
    def time_left(self):
        """ returns the work or break time left"""
        return self.done_with_work - time.time()
        
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
        

    def play_alert(self):
        """Plays the time's up alert sound"""
        
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
    

    the_list = [mytimer.work_time , mytimer.down_time]
    
    while True:
        for i in the_list:
            mytimer.start(i)
       
            while not mytimer.is_time_expired():
            
            
                output = mytimer.format_time(mytimer.time_left())
                no_newline_print(output)
        
                time.sleep(1)
                
                no_newline_print("\x08" * len(output))
            
            
            if i == mytimer.work_time:
                print "\n",
                print "Break time!"
        
                mytimer.play_alert()
                
            if i == mytimer.down_time:
                print"\n"
                print "Work time!"
                
                mytimer.play_alert()
                
                
                
class App:
    
    def __init__(self, master):
        
        frame = Frame(master)
        frame.pack()
        
        self.button = Button(frame, text = "Start", fg = "blue", command =
                             pomodoro(0.1, 0.5))
        self.button.pack(side = LEFT)
        
        self.button = Button(frame, text = "Quit", fg = "red", command =
                             frame.quit)
        self.button.pack(side = LEFT)


root = Tk()

app = App(root)

root.mainloop()
root.destroy()
    
    

# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
