"""
In this example you can see how to control the Lighting Impulse 
output, with the calibration of the load and the calibrated output.

Press F1 and turn on the insturment to acces a remote menu config
The EOS is set on EOI but with the termiantor set in empty works.
I change the EOSto CR, restart the insturment, set EOI restart again
and with termination '', started working

You can see on the screen of the instrument the mode, secuence and 
output voltage while measuring
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

RIC422.write("REN")
RIC422.write("SHP LI")
RIC422.write("LIA 500")
RIC422.write("LIP Pos")
RIC422.write("NBRI 5")
RIC422.write("INVL 5")
RIC422.write("MODE SIN") #Single, Recurrent, Sequence
RIC422.write("OUT1 Off")
RIC422.write("OUT2 On")
RIC422.write("OUT3 Off")
RIC422.write("OUT4 Off")
#RIC422.write("CAL") #For impulse modes 
#RIC422.write("TR")
#print("CAL")
RIC422.write("STRT")
print("STAT? command: ",RIC422.query("STAT ?"))
print("sleep")
time.sleep(60)
print("EMSG? command: ",RIC422.query("EMSG?"))
print("STAT? command: ",RIC422.query("STAT ?"))
RIC422.write("STOP") #without this the insturment remain energized and ignore the panel frontal
RIC422.write("GTL") #Without this have to restart the instrument to use in local mode