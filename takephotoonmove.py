import time
import os
import RPi.GPIO as io

io.setmode(io.BCM)

pir_pin =18

io.setup(pir_pin, io.IN)# activate input

while True:
   if io.input(pir_pin):
      print("CAPTURING SOME PEOPLE!!!!")
      os.system('raspistill -vf -hf -o /home/pi/src/walle/images/$(date +"%Y-%m-%d_%H%M%S").jpg')
      time.sleep(.2)