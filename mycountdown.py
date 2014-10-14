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
    
    def __init__(self):
        """ Create a Pomodoro timer.
        
        Parameters:
        work_time : int 
            how much time in minutes you will be working
        down_time : int
            how long in minutes you will be on break
        """
            
        #self.work_time = work_time * 60
        #self.down_time = down_time * 60
        self.done_with_work = time.time()
        self.reset_case = True
        self.is_paused = False
        self.time_of_pause = time.time()
       
        
    def start_timer(self, done_time):
        """ Start the timer."""
        #done_time = done_time * 60
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
        """ Return the time left to count down."""
        return self.time_left() < 0
        

    def play_alert(self):
        """Plays the time's up alert sound"""
        
        pygame.init()
        pygame.mixer.init()
        sounda = pygame.mixer.Sound("backupdings.wav")
        
        sounda.play()
        
    def toggle_pause_timer(self):
        """Pauses the timer"""
        
        if not self.is_paused:
            self.time_of_pause = time.time()
            self.is_paused = True
        elif self.is_paused:
            pause_duration = time.time() - self.time_of_pause
            self.done_with_work += pause_duration
            self.is_paused = False
            
    def reset(self):
        """Resets the timer"""
        self.done_with_work = time.time()
        
def no_newline_print(text):
    """prints a line."""
    sys.stdout.write(text)
    # make sure it gets printedS
    sys.stdout.flush()

    
    
class App(object):
    
    def __init__(self):
        """ __init__ method for the app.
        
        Attributes:
        self.click_list: Represents the number of times the click method 
        has run, it runs when a number is pressed on the gui.
        
        self.output: Represents what gets printed on the label of the gui.
        
        self.actual_seconds: Represents how many seconds the user wants
        counted down, defaults to 0.
        
        self.list_output: What gets printed on the gui as a list, self.output as a list.
        
        self.reset_click_list: Represents the number of times the reset
        method has been run.
        """
        
        self.mytimer = Mycountdown()
        self.root = tk.Tk()
        self.root.title("My Countdown")
        self.textvar = tk.StringVar()
        self.textvar.set("00:00")
        
        self.label = tk.Label(textvariable=self.textvar, font=16).grid(row=0, columnspan=8)
        self.start_button = tk.Button(self.root, text="START", fg="blue",
                                      command=self.toggle_button, width=5)
        self.start_button.grid(row=1, column=1)
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
            button_command = partial(self.click, label)
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
        self.output = "00:00"

        self.actual_seconds = 0
        self.list_output = []
        self.reset_click_list = []
        
       
        
    def gui_countdown(self):
        """ Determines what the GUI does based on the different states of
        being of the timer. """
        
        if not self.mytimer.is_time_expired() and not self.mytimer.is_paused:
            self.output = self.mytimer.format_time(self.mytimer.time_left())
            self.textvar.set(self.output)
            self.root.after(1000, self.gui_countdown)
        
        elif self.mytimer.is_time_expired():
            self.textvar.set("Time's up!")
            self.mytimer.play_alert()
            self.reset_click_list.append('1')

        elif self.reset_click_list == 2 and self.mytimer.is_time_expired():
            self.list_output = "00:00"
            self.textvar.set(self.list_output)
            
        elif self.mytimer.is_paused: 
            #self.output = self.mytimer.format_time(self.mytimer.time_left())
            self.textvar.set(self.output)
            
            
    def reset(self):
        """ Resets the timer.
        
        The first time it is reset it resets the timer to the start amount.
        The second time it resets to "00:00".
        """
        
        self.reset_click_list.append('1')
        print len(self.reset_click_list)
        
        if len(self.reset_click_list) == 2:
            self.reset_click_list = []
            self.click_list = []
            self.output = "00:00"
            self.textvar.set(self.output)
            self.mytimer.reset()
            self.mytimer.is_paused = False
        else:
            if not self.mytimer.is_paused:
                self.mytimer.toggle_pause_timer()
            
            print len(self.reset_click_list)
            self.output = "%s%s:%s%s" %(self.list_output[0], 
                                             self.list_output[1],
                                             self.list_output[2],
                                             self.list_output[3])
            self.textvar.set(self.output)
            return self.output
      
            
        
        
        
    def click(self, number_button):
        """ Determines what to display on the GUI based on what the user
        inputs.
        """
     
        self.click_list.append(number_button)
        
        how_many_clicks = len(self.click_list)
       
        if how_many_clicks <= 4:
            self.list_output = list(self.output)
            if ":" in self.list_output:
                self.list_output.remove(":")
        
            self.list_output = self.list_output[:-how_many_clicks] + self.click_list
            
            
        elif how_many_clicks > 4:
            
            del self.click_list[:-1]
            self.list_output = list(self.output)
            if ":" in self.list_output:
                self.list_output.remove(":")
            
            self.list_output =  self.list_output[:-len(self.click_list)] + self.click_list
            
        
        self.output = "%s%s:%s%s" %(self.list_output[0],self.list_output[1],self.list_output[2],
                                    self.list_output[3])
        
        self.textvar.set(self.output)
        
        return self.output
        
    def compute_actual_seconds(self):
        """ Takes the users input and calculates the exact number of seconds."""
        
        if self.output == "00:00":
            raise ValueError("Please input a time greater than 00:00")
        self.list_output = list(self.output)
        if ":" in self.list_output:
            self.list_output.remove(":")
        
        minutes = self.list_output[0] + self.list_output[1]
        seconds = self.list_output[2] + self.list_output[3]
        
        self.actual_seconds = float((int(minutes) * 60) + int(seconds))
        
        return self.actual_seconds
        
    def start(self):
        """ Starts the countdown on the GUI."""
        
        self.mytimer.start_timer(self.compute_actual_seconds())
        self.gui_countdown()
        self.reset_click_list = []
        
        
    def toggle_button(self, tog=[0]):
        """ Toggles START/PAUSE button."""
        
        tog[0] = not tog[0]
        if tog[0]:
            self.start_button.config(text='PAUSE')
            if self.mytimer.is_paused:
                self.mytimer.toggle_pause_timer()
            self.start()
            print "text says PAUSE, so we are on start"
            print "is_paused should be false"
            print self.mytimer.is_paused
            return self.output
            
        else:
            self.start_button.config(text='START')
            self.mytimer.toggle_pause_timer()
            print "text says START, so we are on pause"
            print "is_paused should be true"
            print self.mytimer.is_paused
            return self.output
            
      
    
if __name__ == "__main__":
    
    app = App()
    #app.start()
    app.root.mainloop()
    
    
# change format to 00:00:00
# figure out why it says that there is no soundcard
# Need to have this looked at, errors or places to fix things pointed out.
