"""
This code show how to generate a AC voltage waveform and change the frequency (in frequency sweep) 
with the Tektronix AFG1062 connected through USB
"""

import pyvisa
import time

rm=pyvisa.ResourceManager()
rml=rm.list_resources()

AFG1062=rm.open_resource("USB0::0x0699::0x0353::1742233::INSTR")
print("ID: ",AFG1062.query("*IDN?"))

#Frecuency values [Hz]
st_frec=1000
end_frec=100_000
step_frec=1000

#General configuration
AFG1062.write("*RST")
AFG1062.write("*WAI")
AFG1062.write("OUTPut1:STATe OFF") #ON OFF or 1 0
AFG1062.write("OUTPut2:STATe OFF")  #CH2

#channel configuration
AFG1062.write("OUTPut1:IMPedance INFinity") #special mode 
AFG1062.write("SOURce1:FUNCtion:SHAPe SIN") #SIN SQU RAMP PULS y arb
AFG1062.write("SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 2") #Vpk-pk 2.0 or 2e-1 Also valid
AFG1062.write("SOURce1:VOLTage:LEVel:IMMediate:OFFSET 0.006") #6mV or 6V or 6 or 6e-3
AFG1062.write("SOURce1:FREQuency:FIXed "+str(st_frec))

#Enable Output
AFG1062.write("OUTPut1:STATe ON") #CH1

try:
  #Measuring loop
  for i in range(st_frec,end_frec,step_frec):
    AFG1062.write("SOURce1:FREQuency:FIXed "+str(i)) #Set frecuency
    time.sleep(1) #delay to stabilize the output
    
    #Measure instrument commands
  #Output secuence
  AFG1062.write("OUTPut1:STATe OFF")
  AFG1062.write("OUTPut2:STATe OFF")
  
except Exception as error:
  print("Error ocurred, Output secuence")
  print("The error is: ",error)

  #Output secuence
  AFG1062.write("OUTPut1:STATe OFF")
  AFG1062.write("OUTPut2:STATe OFF")

"""
Output:
-------

"""



