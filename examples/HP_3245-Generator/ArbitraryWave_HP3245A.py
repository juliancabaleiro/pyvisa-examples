"""
How to generate Arbitrary Doble exponential/LI-Impulse
Waveform with HP-3245A Universal Source using PyVISA.
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

#Waveform Calculation 
#Must be 2048 points -1 <Real or int< 1 
# 0 ohm  0.03125 Vp-p <V< 20 Vp-p
# 50 ohm  0.015625 Vp-p <V< 10 Vp-p
# In current waveform 0.0001 A <I< 0.2 A
# Each waveform array point is multiplied 
#by the peak value of the peak-to-peak amplitud specified(RANGE)

def trunc_dec(values, decs=0):
    """
    Truncate specified decimals in number less than one
    """
    return np.trunc(values*10**decs)/(10**decs)

#Doble exponential /LI_FULL signal building
#parameters
U=1 #Voltage peak [V]
T1=0.2E-6 #Positive exp cte [s]
T2=50E-6 #Negative exp cte [s]
Tmax=np.log(T2/T1)/(1/T1-1/T2)
d=1/(np.exp(-Tmax/T2) -np.exp(-Tmax/T1))
Ts=200E-6 #Time window or Time period [s]
N=2048 #Total of samples per generation, defined by the Insutrument
fg=1/Ts 
print("Frecuency to set in FREQ command: ",fg)

x = np.linspace(0.0, Ts, N, endpoint=False)
y= U*d*(np.exp(-x/T2)-np.exp(-x/T1)) #LI-FULL calculation

values=""
#Generate the string array
for i in trunc_dec(y,decs=4):
    values=values+str(i)+","
values=values[:-1]

HP3245A.write("OUTBUF ON")
HP3245A.write("REAL VOUT(2047)")
#HP3245A.timeout=20_000 # If you want more than 4 digits need more time to load the values
HP3245A.write("FILL VOUT "+values)
HP3245A.write("FREQ "+str(fg)) #frecuency that repit the 2048 samples

try:
    #chanel A waveform
    HP3245A.write("USE 0") #ch A -> USE 0 or USE CHANA ch B -> USE 100 or USE CHANB
    HP3245A.write("TERM REAR")
    HP3245A.write("RANGE 5")
    HP3245A.write("APPLY WFV 5,VOUT")

    #time.sleep(20)

    HP3245A.write("USE 0")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")
    
except:
    #open Ch A
    HP3245A.write("USE 0")
    HP3245A.write("TERM OPEN") #OPEN or OFF
    HP3245A.write("APPLY DCV 0.0")

"""
Output
------

Frecuency to set in FREQ command:  5000.0
"""