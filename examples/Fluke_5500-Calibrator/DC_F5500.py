"""
Simple DC voltage sweep using a Fluke 5500 Multiprocess calibrator
"""

import pyvisa
import time
import os

rm = pyvisa.ResourceManager()
F5500 = rm.open_resource('GPIB0::2::INSTR')
print("ID: ",F5500.query("*IDN?"))

#Test Values
DC_or=[-1000,-800,-500,-200,0,200,500,800,1000]

#Calibrator Setup
F5500.write("*RST")
#F5500.write("EARTH OPEN") #OPEN or TIED
#F5500.write("LOWS OPEN") #OPEN or TIED
F5500.write("DC_OFFSET 0 V")
#F5500.write("LIMIT 750 V, -750 V")

#Measurement instrument configuration

try:
  #Test loop
  for i in DC_or:
    #Calibator set point
    F5500.write("OUT "+str(i)+" V") 
    F5500.write("*CLS") #Sometimes disable the output and generatea error code for safetly
    time.sleep(5) #Time to change the internal circuit (if requerid)
    F5500.write("OPER") #Enable the output
    time.sleep(15) #Settling time in the load
    
    #measure

  #Output secuence
  F5500.write("STBY")
  F5500.write("OUT 0 V, 0 Hz") 
except Exception as error:
  print("Error ocurred, Output secuence")
  print("The error is: ",error)

  #Output secuence
  F5500.write("STBY")
  F5500.write("OUT 0 V, 0 Hz") 