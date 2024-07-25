"""
How to generate one sine wave per channel and connect
CHA in rear panel, CHB in front pannel and open the channels
separatly with HP3445A Universal Source using PyVISA.
This device use HP-IB a old version of GP-IB 
for this reason have different commands and 
need the termination set for correct communication
"""

import pyvisa
import time
import numpy as np

print("\n")
rm = pyvisa.ResourceManager()
HP3245A=rm.open_resource("GPIB0::5::INSTR")
#Set the end of the line 
HP3245A.read_termination = '\n'
HP3245A.write_termination = '\n'
HP3245A.write("RESET")
HP3245A.write("CLR")
HP3245A.write("SCRATCH")
HP3245A.write("BEEP OFF")
#ACI,ACV,DCI,DCV,DCMEMI,DCMEMV,RPI,RPV,SQI,SQV,WFI,WFV
print("APPLY? command: ",HP3245A.query("APPLY?"))
a_pk=1*np.sqrt(2)*2
frec=500
offset=0
try:
    #chanel A waveform
    HP3245A.write("USE 0") #ch A -> USE 0 or USE CHANA ch B -> USE 100 or USE CHANB
    HP3245A.write("TERM OPEN")
    HP3245A.write("FREQ "+str(frec))
    HP3245A.write("DCOFF "+str(offset)) #max 50 % of the range
    HP3245A.write("APPLY ACV "+str(a_pk)) # Peak To Peak value
    print("APPLY? command: ",HP3245A.query("APPLY?"))
    HP3245A.write("TERM REAR") #select and connect the panel 
    print("CHA TERM? command: ",HP3245A.query("TERM?"))
    #chanel B waveform
    HP3245A.write("USE 100") #ch A -> USE 0 or USE CHANA ch B -> USE 100 or USE CHANB
    HP3245A.write("TERM OPEN")
    HP3245A.write("FREQ "+str(frec))
    HP3245A.write("DCOFF "+str(offset)) #max 50 % of the range
    HP3245A.write("APPLY ACV "+str(a_pk)) # Peak To Peak value
    HP3245A.write("TERM FRONT") #select and connect the panel 
    print("CHB TERM? command: ",HP3245A.query("TERM?"))

    time.sleep(20)
    #open Ch A
    HP3245A.write("USE 0")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")
    #open Ch B
    HP3245A.write("USE 100")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")
except:
    #open Ch A
    HP3245A.write("USE 0")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")
    #open Ch B
    HP3245A.write("USE 100")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")
"""
APPLY? command:  DCV
APPLY? command:  ACV
CHA TERM? command:   REAR
CHB TERM? command:  FRONT

"""
"""
Measured with oscilloscope CHA: 992 mV CHB:990 mV
"""