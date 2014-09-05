import time
import subprocess
import sys
import Tkinter as tk
import pygame




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
        self.quit_button = tk.Button(self.root, text="QUIT", fg="red", command
                                =self.root.quit)
        self.quit_button.pack(side=tk.LEFT)
        self.mytimer = Mycountdown(5, 25)
        
    def gui_countdown(self):
        
        if not self.mytimer.is_time_expired():
            output = self.mytimer.format_time(self.mytimer.time_left())
            print repr(output)
            self.label.configure(text=output, font=16)
            self.root.after(1000, self.gui_countdown)
            
        else:
            self.label.configure(text="Time's up!")
            self.mytimer.play_alert()
            
            
            
    def start(self):
        
        self.mytimer.start(10)
        self.gui_countdown()
        
       

#def actual_start():
    
if __name__ == "__main__":
    app = App()
    #app.start()
    app.root.mainloop()
    

# want to figure out a way to pause it
# make a GUI
# change format to 00:00:00
# figure out why it says that there is no soundcard
	
