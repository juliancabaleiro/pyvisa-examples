# pyvisa-examples

This repository provides a lot of examples on how to use instruments that support IEEE488.2/SCPI with python 3 using [PyVISA](https://pyvisa.readthedocs.io/en/latest/). Depend on the instrument you can connect with this trough RS-232, GPIB, USB, Ethernet, etc. this is quasi transparent for the user. Most of the examples were developed using GPIB-USB-HS+ adapter, or via USB.  
The idea is to share examples with the simplest possible use of python so as to not lose focus on the programming flow of the device.

## Overview

[PyVISA](https://pyvisa.readthedocs.io/en/latest/) is a very useful tool to automate measurements, calibrations, characterization or tests and combine this with python tools. In this repository you can find examples to program Calibrator's, DMM's, Oscilloscopes, Arbitrary Waveform Generator's, NanoVoltimeter, etc.   
In examples folder, you can find examples to how to use different instruments individually or in combination with another instruments.

## Installation

### Driver

Follow the step in [backend installation](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html#backend), you can install python backend or National instrument (NI), for this examples I use a [NI-VISA](https://www.ni.com/es/support/downloads/drivers/download.ni-visa.html#544206) driver.  
If you want to use NI GPIB-USB-HS+ same have to install [NI-488.2 driver](https://www.ni.com/es/support/downloads/drivers/download.ni-488-2.html#544048).

### Python

- Install an IDE for python, I recomend VS code
- Install Python XXXX
- Create venv 
- Install requeriments.txt
- Run *test_VISA.py* and see the connected instrument in terminal

