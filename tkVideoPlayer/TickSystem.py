import time



# this is a small Module that allowes us to run our any while loop
# exactly set amount of times we want it without worring about other
# lines of the code effecting how many times we run it like in the
# the only limmiting factor becomes if your cpu can handle all the
# proccessing in the while loop that you put in it

class FpsController: # this is a tick system that will help you block the
                     # the main loop up until a certain time
  
    def __init__(self, DesiredFps:int = 60): # we take the DesierdFps
        self.fpsCount:int = 0 # this is for us to keep track of fps
                              # if we want to view it at real time

        self.Tick:float = 1/DesiredFps # intialise the time for the tick
                                       # we are aiming for


        #private Variables
        self.FpsTimer:float = time.time() + 1 # we create a timer if we want
                                              # this will help us view the
                                              # images our selfs

        self.TickTimer:float = time.time()  # this help us keep track of how 
                                            # much time has passed by adding
                                            # the tick we made


    def BlockUntilNextFrame(self):
        while True: # this blockes the functions when you run it through a while loop
            
            if self.Tick <= (time.time() - self.TickTimer): # this will check if more
                                                            # time has passed than our
                                                            # tick if that is the case
                                                            # add the tick to the 
                                                            # ticktimer and unblock the
                                                            # function  we  blocked  by
                                                            # running this function 
                self.TickTimer += self.Tick
                return

            time.sleep(1/1000) # sleep for one milliseconds
                               # we do this so we dont over
                               # stress the cpu by the while
                               # loop 


    def ShowFps(self): # this function will simply show the fps
        self.fpsCount += 1 # this will keep count of the fps 
        if time.time() >= self.FpsTimer: # check if it hase been 
                                         # 1 sec
            print(self.fpsCount) # print out the fps

            self.fpsCount = 0  # reset the fps
            self.FpsTimer = time.time() + 1 # reset the timer