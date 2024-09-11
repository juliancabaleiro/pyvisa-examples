"""
How to control this HP3445A Universal Source using PyVISA.
This device use HP-IB a old version of GP-IB 
for this reason have different commands and 
need the termination set for correct communication
"""

import pyvisa
import time
import os
import numpy as np
import pandas as pd

print("\n")
rm = pyvisa.ResourceManager()
HP3245A=rm.open_resource("GPIB0::5::INSTR")
#Set the end of the line 
HP3245A.read_termination = '\n'
HP3245A.write_termination = '\n'
HP3245A.write("RESET")
HP3245A.write("CLR")
print("General query command")
print("ID? command: ",HP3245A.query("ID?"))
print("IDN? command: ",HP3245A.query("IDN?"))
#For example this command generates a error code 2
print("IMP? command: ",HP3245A.query("IMP?"))
print("ERR? command: ",HP3245A.query("ERR?"))
print("ADDR? command: ",HP3245A.query("ADDR?"))
print("OUTPUT? command: ",HP3245A.query("OUTPUT?"))
print("PAUSED? command: ",HP3245A.query("PAUSED?"))
print("RANGE? command: ",HP3245A.query("RANGE?"))
print("READY? command: ",HP3245A.query("READY?"))
print("REFIN? command: ",HP3245A.query("REFIN?"))
print("REV? command: ",HP3245A.query("REV?"))
print("SER? command: ",HP3245A.query("SER?"))
print("TERM? command: ",HP3245A.query("TERM?"))
print("TRIGMODE? command: ",HP3245A.query("TRIGMODE?"))
print("USE? command: ",HP3245A.query("USE?"))
print("APPLY? command: ",HP3245A.query("APPLY?"))

"""
Output:
-------


General query command
ID? command:  HP3245
IDN? command:  HEWLETT PACKARD
IMP? command:       0
ERR? command:       0
ADDR? command:       5
OUTPUT? command:   0.0000000E+00
PAUSED? command:       0
RANGE? command:   1.0000000E+00
READY? command:       1
REFIN? command:  INT
REV? command:    2843
SER? command:  0000A00000
TERM? command:  FRONT
TRIGMODE? command:     OFF
USE? command:       0
APPLY? command:  DCV
"""