# pyvisa-examples

This repository provides a lot of examples on how to use instruments that support IEEE488.2/SCPI with python 3 using [PyVISA](https://pyvisa.readthedocs.io/en/latest/). Depend on the instrument you can connect with this trough RS-232, GPIB, USB, Ethernet, etc. this is quasi transparent for the user. Most of the examples were developed using GPIB-USB-HS+ adapter, or via USB.  
The idea is to share examples with the simplest possible use of python so as to not lose focus on the programming flow of the device.

## Overview

[PyVISA](https://pyvisa.readthedocs.io/en/latest/) is a very useful tool to automate measurements, calibrations, characterization or tests and combine this with python tools. In this repository you can find examples to program **Calibrator's**, **DMM's**, **Oscilloscopes**, A**rbitrary Waveform Generator's**, **NanoVoltimeter**, etc.   
In examples folder, you can find examples to how to use different instruments individually or in combination with other instruments using the simplest python possible.  
The idea is to share examples with the simplest possible use of python so as to not lose focus on the programming flow of the device.     
Aditionally, a **Dash folder** contain a simple GUI developed in python using [Dash-plotly](https://plotly.com/examples/) to make measurements. For more examples you can see [nidaqmx-python-examples](https://github.com/juliancabaleiro/nidaqmx-python-examples/tree/main/examples/dash) 

## Installation

### Driver

Follow the step in [backend installation](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html#backend), you can install python backend or National instrument (NI), for this examples I use a [NI-VISA](https://www.ni.com/es/support/downloads/drivers/download.ni-visa.html#544206) driver.  
If you want to use NI GPIB-USB-HS+ same have to install [NI-488.2 driver](https://www.ni.com/es/support/downloads/drivers/download.ni-488-2.html#544048).  
In my case I used:
- **NI max** version: 2023 Q4
- **NI VISA** version: 2024 Q1
- **NI IEEE 488.2** version: 2023 Q3

### Check instruments in NI-MAX

With the installation of the NI driver the NI-MAX is installed, there you can list all instruments connected with the computer and communicate to check the correct installation.

![Alt Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/nimax-devices.png)

Click on the instrument and then on *test panel button* to communicate with the instrument, typically we make a query **IDN?* like *Hello world!* message to obtain the model of the instrument.

![Alt Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/test-visa-panel.png)

### Python

- Install an IDE for python, I recomend **Visual Studio code**
- Install **Python 3.10.11 64 bits** (I used this version)
- Create **venv** 
- Install **requeriments.txt**
- Run **test_VISA.py** and see the connected instrument in terminal

