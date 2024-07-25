"""
Press F1 and turn on the insturment to acces a remote menu config
The EOS is set on EOI but with the termiantor set in empty works.
I change the EOSto CR, restart the insturment, set EOI restart again
and with termination '', started working

You can see on the screen of the instrument the mode and output voltage
while measuring
"""

import pyvisa
import time
import os
import numpy as np
import pandas as pd

rm = pyvisa.ResourceManager()
#print(rm.list_resources())
RIC422=rm.open_resource("GPIB0::11::INSTR")
RIC422.read_termination = ''
RIC422.write_termination = ''
RIC422.write("TMO 9")
print("ID? command: ",RIC422.query("ID ?"))
print("EMSG? command: ",RIC422.query("EMSG ?"))
#print("STAT? command: ",RIC422.query("STAT"))
#print("STAT? command: ",RIC422.query("ERR?;"))
RIC422.write("REN")
RIC422.write("SHP DC")
RIC422.write("DCA 200")
RIC422.write("INVL 5")
RIC422.write("OUT1 Off")
RIC422.write("OUT2 On")
RIC422.write("OUT3 Off")
RIC422.write("OUT4 Off")
#RIC422.write("TR")
RIC422.write("STRT")
print("Pause to measure")
time.sleep(10)
print("EMSG? command: ",RIC422.query("EMSG?"))
print("STAT? command: ",RIC422.query("STAT ?"))
RIC422.write("STOP") #without this the insturment remain energized and ignore the panel frontal
RIC422.write("GTL")
"""
Output
------
ID? command:  RIC 422 3.3 
EMSG? command:    0
Pause to measure
EMSG? command:    0
STAT? command:  CAL
"""