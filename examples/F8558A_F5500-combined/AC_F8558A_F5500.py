"""
Frecuency response using Fluke 5500 and Fluke 8558A
and save the data in .xlsx
"""

import pyvisa
import time
import os
import numpy as np
import pandas as pd

file_name = os.path.basename(__file__)

rm = pyvisa.ResourceManager()
F8558_address="USB0::0x0F7E::0x8009::624282630::INSTR"
F8558=rm.open_resource(F8558_address)
F5500 = rm.open_resource('GPIB0::2::INSTR')
print("Calibrator: ",F5500.query("*IDN?"))
print("DMM: ",F8558.query("*IDN?"))

#Test Values
AC_rms=10
AC_frec=[50,60,100,500,1_000,2_000,5_000,6_000,8_000,10_000,50_000,100_000]
#AC_frec=[50,60]

#Fluke 5500 calibrator configuration
F5500.write("*RST")
F5500.write("EARTH OPEN") #OPEN or TIED
F5500.write("LOWS OPEN") #OPEN or TIED
F5500.write("DC_OFFSET 0 V")
F5500.write("LIMIT 750 V, -750 V")

#Fluke 8558A DMM configuration
F8558.write("*RST")
F8558.write("INIT:CONT OFF") #stop trigger
F8558.write("DISPlay ON")
F8558.timeout = 50000

#channel 
F8558.write("ROUT:TERM FRON") #FROM or REAR
F8558.write("ROUT:INP:GUAR OFF") # ON or OFF
#Volt
F8558.write("SENS:FUNC \"VOLTage:AC\"")
F8558.write("SENSe:VOLTage:AC:BWIDth WIDE")
F8558.write("SENSe:VOLTage:AC:COUPling:SIGNal AC1M")
F8558.write("SENSe:VOLTage:AC:COUNter:COUPling AC")
F8558.write("SENSe:VOLTage:AC:RESolution MIN")
F8558.write("SENSe:VOLTage:AC:RANGe 10")

#trigger
F8558.write("TRIGger:SOURce TIMer")
F8558.write("TRIGger:TIMer 0.5") #timer time or trigger time
F8558.write("TRIGger:COUNt 10") #trigger counts or #samples
F8558.write("TRIGger:DELay:AUTO OFF")
F8558.write("TRIGGER:DELay 0")

v_mean=np.array([])
v_std=np.array([])
aux=np.array([])

#Measure loop
try:
  for i in AC_frec:
    print("Current frecuency: ", i)
    #Calibrator Configuration
    F5500.write("OUT "+str(AC_rms)+" V, "+str(i)+" Hz") 
    F5500.write("*CLS")
    time.sleep(5) #To change the board if required
    F5500.write("OPER")
    time.sleep(15) #To stabilize the value
    #Measure secuence
    aux=F8558.query_ascii_values("READ?", container=np.array) #numpy.ndarray
    #save the data
    v_mean=np.append(v_mean,np.mean(aux))
    v_std=np.append(v_std,np.std(aux))

  #Output secuence
  F5500.write("STBY") #In high current output is recomended lower the current slowly
  F5500.write("OUT 0 V, 0 Hz")
  F8558.write("SENSe:VOLTage:AC:RANGe 1000")

  #data management
  data_d={"frecuency[Hz]":AC_frec,
        "mean[V]":v_mean,
        "std[V]":v_std}

  data_df=pd.DataFrame(data_d)
  print(data_df)
  barra="\9"
  path=r"caracterisation\data"+barra[0]+file_name[:-3]+".xlsx"
  data_df.to_excel(path,index=False)
    
except Exception as error:
  print("Error ocurred, Output secuence")
  print("The error is: ",error)

  #Calibrator output secuence
  F5500.write("STBY") #In high current output is recomended lower the current slowly
  F5500.write("OUT 0 V, 0 Hz") 
  #multimeter output secuence
  F8558.write("SENSe:VOLTage:AC:RANGe 1000")

"""
Output
------

Calibrator:  FLUKE,5500A,7215002,2.4+1.3+2.0+*

DMM:  FLUKE,8558A,624282630,1.31

Current frecuency:  50
Current frecuency:  60
Current frecuency:  100
Current frecuency:  500
Current frecuency:  1000
Current frecuency:  2000
Current frecuency:  5000
Current frecuency:  6000
Current frecuency:  8000
Current frecuency:  10000
Current frecuency:  50000
Current frecuency:  100000
    frecuency[Hz]   mean[V]    std[V]
0              50  9.999691  0.000040
1              60  9.999728  0.000017
2             100  9.999938  0.000069
3             500  9.999732  0.000059
4            1000  9.999599  0.000056
5            2000  9.999561  0.000039
6            5000  9.999479  0.000020
7            6000  9.999551  0.000045
8            8000  9.999206  0.000033
9           10000  9.999285  0.000025
10          50000  9.998142  0.000008
11         100000  9.998762  0.000018
"""