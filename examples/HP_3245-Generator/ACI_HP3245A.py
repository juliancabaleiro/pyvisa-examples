"""
How to generate a current sinewave with HP3445A Universal Source using PyVISA.
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
a_pk=60E-3*np.sqrt(2)*2
frec=5000
offset=1
HP3245A.write("USE 0") #ch A -> USE 0 or USE CHANA ch B -> USE 100 or USE CHANB
HP3245A.write("FREQ "+str(frec))
HP3245A.write("APPLY ACI "+str(a_pk)) # Peak To Peak value
print("APPLY? command: ",HP3245A.query("APPLY?"))
time.sleep(20)
HP3245A.write("APPLY DCV 0.0")

"""
Output
------

APPLY? command:  DCV
APPLY? command:  ACI
"""
"""
Measured with Keysigth U1232A multimeter 0.060 A
"""