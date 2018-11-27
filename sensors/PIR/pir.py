import time
import os
import RPi.GPIO as io

io.setmode(io.BCM)
 
pir_pin =18
  
io.setup(pir_pin, io.IN)# activate input
  
while True:
   if io.input(pir_pin):
      print("CAPTURING!")
      os.system('raspivid -o /home/pi/src/walle/images/$(date +"%H%M%S").h264 -t 10000')

      time.sleep(.5)

