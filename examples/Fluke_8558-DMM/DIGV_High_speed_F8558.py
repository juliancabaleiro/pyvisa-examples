"""
Simple acquisition Fluke 8558A in voltage Digitize mode
with high speed transfer data.
Transfer the data in binary form, using USB 

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
F8558.timeout = 50000

print("\nID: ",F8558.query("*IDN?"))

#Fluke 8558 configuratrion
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
#High speed mode
F8558.write("DISP OFF")
print("DISP state: ",F8558.query("DISP?"))
F8558.write("CALCulate:SSTatistics:STATe OFF")
print("STATS: ",F8558.query("CALCulate:SSTatistics:STATe?"))
F8558.write("SYSTem:PRESet FAST") #no query command
F8558.write("FORMat:DATA PACKed,4") #no query command

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

# scale factor query
scale_f=float(F8558.query("FORMat:DATA:SCALE?"))
print("Scale: ",scale_f)

# Current source manually setup
print("Configure the voltage source and press enter: ")
input()

#Launch trigger
start = time.time()
F8558.write("INIT:CONT ON")
#Read 
data=F8558.query_binary_values("READ?",
                                datatype="i",
                                is_big_endian=True,
                                container=np.ndarray)
finish = time.time()

l_data=len(data)
print("\nTime READ command: ",finish-start)
print("Data length: ",l_data)
print("Data type: ", type(data))
print("Data raw: ",data[:5])
data=data*scale_f
print("Data scaled: ",data[:5])

#save in csv
df=pd.DataFrame(data)
df.to_csv(r"F8558\files\data.csv", header=False, index=False)

ts=1E-6
t=np.linspace(0.0, l_data*ts, l_data, endpoint=False)

#Plot data
fig, ax = plt.subplots()
ax.plot(t,data)
ax.set(xlabel='Time [s]', ylabel='Voltage [V]',
       title='Voltage Digitize High speed mode Fluke 8558A')
ax.grid()
fig.savefig(r"F8558\files\data.png")

plt.show()

#normal mode: 43.637638568878174 s
#super fast mode 4.463783025741577 s

"""
Output
------

ID:  FLUKE,8558A,624282630,1.31

DISP state:  0

STATS:  0

Scale:  1.0124046414e-08
Configure the voltage source and press enter: 


Time READ command:  4.42468786239624
Data length:  1000000
Data type:  <class 'numpy.ndarray'>
Data raw:  [233377792 233279488 233422848 233336832 233377792]
Data scaled:  [2.3627276  2.36173236 2.36318375 2.36231292 2.3627276 ]

"""