# Haefely RIC 422 Impulse Calibrator

This is High voltage impulse calibrator can generate a Lightning Full, Lighting Front Chopped, Switching Impulse, DC and step waveforms. For more info you can read the [Reference Manual](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/Haefely-RIC-422-Reference-IMpulse-Calibrator-Version-1.0.pdf).

> **Danger**  
> If communication fails regardless of why the instrument remains in the last state, probably with the output on and in remote mode, having to restart it manually or reestablishing communication to turn off the output.  
For to avoid this, ever you need to contain the possible errors and use a safe exit sequence.


## Configure the communication

Press F1 and turn On the instrument to acces the communication menu, there you can configure this in GPIB, EOS (End of String) and the address.
Then you have to configure the termination in *''* PyVISA.  
This instrument is old, it has its own commands that are different from the current ones, there are few commands and they are found in the Reference Manual.

## DC_RIC422.py

In this example you can see how to control the DC output.

## LI-FULL_RIC422.py

In this example you can see how to control the Lighting Impulse output, with the calibration of the load and the calibrated output.

