import time
import subprocess
import sys
import Tkinter as tk
import pygame
from functools import partial
import string
import re





class Mycountdown(object):
    
    def __init__(self, work_time, down_time):
        """ Create a Pomodoro timer.
        
        Parameters:
        work_time : int 
            how much time in minutes you will be working
        down_time : int
            how long in minutes you will be on break
        """
            
        self.work_time = work_time * 60
        self.down_time = down_time * 60
        self.done_with_work = time.time()
        self.reset_case = True
       
        
    def start_timer(self, done_time):
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
            the time left in seconds. 
        """
        
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
        
    def pause_timer(self):
        """Pauses the timer"""
        
            
        
        
def no_newline_print(text):
    sys.stdout.write(text)
    # make sure it gets printedS
    sys.stdout.flush()

    
    
class App(object):
    
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="00:00", font=16).grid(row=0, columnspan=6)
        self.start_button = tk.Button(self.root, text="START", fg="green",
                                      command=self.start).grid(row=1, column=0, 
                                      sticky=tk.E)
        self.reset_button = tk.Button(self.root, text="RESET", fg="yellow",
                                      command=self.reset).grid(row=1,
                                      column=1)
        self.quit_button = tk.Button(self.root, text="QUIT", fg="red",
                                      command=self.root.quit,width=5).grid(row=1,
                                      column=2, sticky=tk.E)
        lf = tk.LabelFrame(self.root, text="Keypad", bd=3, 
                           relief=tk.RIDGE).grid(columnspan=3)
        #lf.pack(side=tk.BOTTOM)
        self.button_list = [
        '7','8','9',
        '4','5','6',
        '1','2','3',
        '0']
        r = 4
        c = 0
        n = 0
        number_button = list(range(len(self.button_list)))
        for label in self.button_list:
            cmd = partial(self.click, label)
            number_button[n] = tk.Button(lf, text=label, width=5, command=cmd)
            number_button[n].grid(row=r, column=c)
            n += 1
            c += 1
            if c > 2:
                c = 0
                r +=1
            if n == 9:
                c = 1
        self.mytimer = Mycountdown(5, 25)
       
        
    def gui_countdown(self):
        
        
        if not self.mytimer.is_time_expired() and self.mytimer.reset_case:
            print type(self.label)
            output = self.mytimer.format_time(self.mytimer.time_left())
            print repr(output)
            print self.mytimer.reset_case
            self.label.configure(text=output, font=16)
            self.root.after(1000, self.gui_countdown)
        
        if self.mytimer.is_time_expired():
            self.label.configure(text="Time's up!")
            self.mytimer.play_alert()
            print self.mytimer.reset_case
        
        if not self.mytimer.reset_case:
            self.label.configuretext=("00:00")
        
        if not self.mytimer.reset_case and self.mytimer.is_time_expired():
            self.label.configure(text="00:00")
            
    def reset(self):
        self.mytimer.reset_case = False
        print self.mytimer.reset_case
        print self.mytimer.is_time_expired()
        return self.mytimer.reset_case
        
            
    def start(self):
        
        self.mytimer.start_timer(5)
        self.gui_countdown()
        
    def click(self, number_button):
        s = "%s" % number_button
        output = "00:00"
        for i in range(1, len(output)):
            
            output = output.replace(output[len(output)-i], s)

            self.label.configure(text=output)
            break
      
    
if __name__ == "__main__":
    app = App()
    #app.start()
    app.root.mainloop()
    

# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
