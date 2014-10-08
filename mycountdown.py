import time
import subprocess
import sys
import Tkinter as tk
import pygame
from functools import partial
import string
import re
import tkFont


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
        self.pause_case = False
       
        
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
        self.mytimer = Mycountdown(5, 25)
        self.root = tk.Tk()
        self.root.title("My Countdown")
        self.textvar = tk.StringVar()
        self.textvar.set("00:00")
        self.count = []
        
        self.label = tk.Label(textvariable=self.textvar, font=16).grid(row=0, columnspan=8)
        self.start_button = tk.Button(self.root, text="START", fg="blue",
                                      command=self.toggle_button, width=5)
        self.start_button.grid(row=1, column=1)
        #self.start_button.pack(pady=5)
        self.reset_button = tk.Button(self.root, text="RESET", fg="yellow",
                                      command=self.reset, width=5)
        self.reset_button.grid(row=1, column=2)
        self.quit_button = tk.Button(self.root, text="QUIT", fg="red",
                                      command=self.root.quit,width=5)
        self.quit_button.grid(row=1, column=3)
        lf = tk.LabelFrame(self.root, text="Keypad", bd=3, 
                           relief=tk.RIDGE).grid(columnspan=3)
        self.button_list = [
        '1','2','3',
        '4','5','6',
        '7','8','9',
        '0']
        row = 4
        column = 1
        n = 0
        number_button = list(range(len(self.button_list)))
        for label in self.button_list:
            button_command = partial(self.click, label, len(self.count))
            number_button[n] = tk.Button(lf, text=label, width=5, command=button_command)
            number_button[n].grid(row=row, column=column)
            n += 1
            column += 1
            if column > 3:
                column = 1
                row +=1
            if n == 9:
                column = 2
        
        
        self.click_list = []
        self.output = "0000"
        self.actual_seconds = 0
        self.list_output = "00:00"
        self.reset_click_list = []
        
       
        
    def gui_countdown(self):
        
        # if True and False
        if self.mytimer.reset_case and not self.mytimer.is_time_expired() and not self.mytimer.pause_case:
            print "reset_case TRUE time_expired FALSE first"
            output = self.mytimer.format_time(self.mytimer.time_left())
            print repr(output)
            self.textvar.set(output)
            self.root.after(1000, self.gui_countdown)
        
        # if True
        elif self.mytimer.is_time_expired():
            print "time_expired TRUE second"
            self.textvar.set("Time's up!")
            self.mytimer.play_alert()
            self.reset_click_list.append('1')
            print self.mytimer.reset_case
        
        # if False
        elif not self.mytimer.reset_case:
            print "reset_case FALSE third"
        
        # if False and True
        elif not self.mytimer.reset_case and self.mytimer.is_time_expired():
            print "reset_case FALSE time_expired TRUE fourth"
            self.textvar.set("00:00")
            
        elif self.mytimer.pause_case: 
            output = self.mytimer.format_time(self.mytimer.time_left())
            self.textvar.set(output)
            
            
    def reset(self):
        self.reset_click_list.append('1')
        print len(self.reset_click_list)
        if len(self.reset_click_list) == 2:
            self.reset_click_list = []
            self.click_list = []
            self.list_output = "00:00"
            self.textvar.set(self.list_output)
            self.mytimer.reset_case = True
            self.mytimer.pause_case = False
        else:
            print len(self.reset_click_list)
            self.list_output = "%s%s:%s%s" %(self.list_output[0], 
                                             self.list_output[1],
                                             self.list_output[2],
                                             self.list_output[3])
            self.textvar.set(self.list_output)
            
            self.mytimer.reset_case = False
            
        return self.mytimer.reset_case
        
        
        
    def click(self, number_button, count):
     
        self.click_list.append(number_button)
        
        how_many_clicks = len(self.click_list)
       
        if how_many_clicks <= 4:
            self.list_output = list(self.output)
        
            self.list_output = self.list_output[:-how_many_clicks] + self.click_list
            
            
        elif how_many_clicks > 4:
            
            del self.click_list[:-1]
            self.list_output = list(self.output)
            
            self.list_output =  self.list_output[:-len(self.click_list)] + self.click_list
            
        
        self.list_output = "%s%s:%s%s" %(self.list_output[0],self.list_output[1],self.list_output[2],
                                    self.list_output[3])
        print self.list_output
        self.textvar.set(self.list_output)
        
        return self.list_output
        
    def compute_actual_seconds(self):
        
        if self.list_output == "00:00":
            raise ValueError("Please input a time greater than 00:00")
        self.list_output = list(self.list_output)
        if ":" in self.list_output:
            self.list_output.remove(":")
        
        minutes = self.list_output[0] + self.list_output[1]
        seconds = self.list_output[2] + self.list_output[3]
        
        self.actual_seconds = float((int(minutes) * 60) + int(seconds))
        
        return self.actual_seconds
        
    def start(self):
        
        self.mytimer.start_timer(self.compute_actual_seconds())
        self.gui_countdown()
        
    def pause(self):
        print "the pause button has been pressed"
        print "this is the current output %s" % self.mytimer.format_time(self.mytimer.time_left())
        
        self.mytimer.pause_case = True
        
        return self.mytimer.pause_case
        
    def toggle_button(self):
        if self.start_button.config('text')[-1] == 'START':
            self.start_button.config(text='PAUSE')
            self.start()
        else:
            self.start_button.config(text='START', command=self.start)
            self.pause()
      
    
if __name__ == "__main__":
    
    app = App()
    #app.start()
    app.root.mainloop()
    
    
    

# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
