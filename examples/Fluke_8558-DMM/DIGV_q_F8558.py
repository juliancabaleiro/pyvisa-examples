"""
Simple acquisition Fluke 8558A in voltage Digitize mode.
query method

Connection
----------
External trigger [HP-3245A]: 5 Vpk-pk; 2.5 Voffset; 10 kHz
Voltage Input [Fluke 5500]: 5 Vrms 10 Hz
"""
import pyvisa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

rm=pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)

print("ID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"DIG:VOLT\"")
F8558.write("SENS:DIG:VOLT:COUP:SIGN DC10M")
F8558.write("SENS:DIG:VOLT:RANG 10")
F8558.write("SENS:DIG:FILT 3MHZ")

#Aperture time
F8558.write("SENS:DIG:APER 7E-7")

#Arm setup
F8558.write("ARM:LAY2:SOUR IMM")
F8558.write("ARM:LAY2:COUN 1") #count trigger 2
F8558.write("ARM:LAY2:DEL:AUTO OFF")
F8558.write("ARM:LAY2:DEL 0")
F8558.write("ARM:LAY1:SOUR EXT")
F8558.write("ARM:LAY1:COUN 1") #count trigger 1
F8558.write("ARM:LAY1:DEL:AUTO OFF")
F8558.write("ARM:LAY1:DEL 0")

# #samples=count_tri1*Count_trig2
# Max samples: 5e6 with timestamp
# Max samples: 10e6 without timestamp

#trigger

F8558.write("TRIG:SOUR TIM")
F8558.write("TRIG:TIM 1E-6") #frec sample in 
F8558.write("TRIG:COUN 1E6")
F8558.write("TRIG:DEL:AUTO OFF")
F8558.write("TRIG:DEL 0")
F8558.write("TRIG:HOLD OFF")

# Current source manually setup
print("Configure the voltage source and press enter: ")
input()

#Launch trigger
start = time.time()
F8558.write("INIT:CONT ON")
#Read 
data=F8558.query("READ?") #String representation of dictionary
finish = time.time()

l_data=len(data)
print("Time READ command: ",finish-start)
print("Data length: ",l_data)
print("Data type: ", type(data))
#print("Data raw: ",data[0:5])

#save in csv
df=pd.DataFrame(eval(data))
df.to_csv(r"F8558\files\data.csv", header=False, index=False)

ts=1E-6
t=np.linspace(0.0, l_data*ts, l_data, endpoint=False)

#Plot data
fig, ax = plt.subplots()
ax.plot(t,data)
ax.set(xlabel='Time [s]', ylabel='Voltage [V]',
       title='Voltage Digitize with Fluke 8558A')
ax.grid()
fig.savefig(r"F8558\files\data.png")
plt.show() 

"""
Output
------
ID:  FLUKE,8558A,624282630,1.31

Time READ command:  42.419824838638306
Data length:  1000000
Data type:  <class 'numpy.ndarray'>
Data raw:  [3.9437  3.93864 3.93806 3.93905 3.93943]
"""