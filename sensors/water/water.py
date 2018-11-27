import time
import os
import RPi.GPIO as io

io.setmode(io.BCM)
 
pin = 27
  
io.setup(pin, io.IN) # activate input

  
while True:
    print io.input(pin)
    time.sleep(.5)

