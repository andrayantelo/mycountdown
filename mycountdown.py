import time
import subprocess
import sys
import Tkinter as tk
import pygame
from functools import partial




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
        self.label = tk.Label(text="null")
        self.label.pack()
        self.label.configure(text="00:00", font=16)
        self.start_button = tk.Button(self.root, text="START", fg="green", 
                                      command=self.start)
        self.start_button.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self.root, text="RESET", fg="yellow",
                                     command=self.reset)
        self.reset_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self.root, text="QUIT", fg="red", command
                                =self.root.quit)
        self.quit_button.pack(side=tk.LEFT)
        lf = tk.LabelFrame(self.root, text="Keypad", bd=3) 
        lf.pack(padx=15, pady=10)
        self.button_list = [
        '7','8','9',
        '4','5','6',
        '1','2','3',
        '0']
        r = 1
        c = 0
        n = 0
        btn = list(range(len(self.button_list)))
        for label in self.button_list:
            cmd = partial(self.click, label)
            btn[n] = tk.Button(lf, text=label, width=5, command=cmd)
            btn[n].grid(row=r, column=c)
            n += 1
            c += 1
            if c > 4:
                c = 0
                r +=1
        self.mytimer = Mycountdown(5, 25)
       
        
    def gui_countdown(self):
        
        
        if not self.mytimer.is_time_expired() and self.mytimer.reset_case:
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
            self.label.configure(text="00:00")
        
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
        
    def click(self, btn):
        s = "%s" % btn
        output = "00:00"
        for letter in output:
            self.label.configure(text="00:0%s"% s)
       # self.root.title(s)
    
if __name__ == "__main__":
    app = App()
    #app.start()
    app.root.mainloop()
    

# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
