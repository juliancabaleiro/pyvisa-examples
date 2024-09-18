# Fluke 8558 -8 1/2 digit's Digital Multimeter

This high precision digital multimeter has one channel with which it can measure DC voltage, AC voltage, DC current, AC current, resistance, frequency, temperature.   
Especially this instrument has the **Digitize** mode with which it allows to digitalize arbitrary voltage or current waveforms.

## Configure the communication

The instrument was configured for USB communication. This instrument can be configured in **High Speed mode**, this allows with some additionally configuration to transfer the data in binary form to achieve better communication times.  
For 1 MHz sampling frequency, 1 s acquisition time:
| Mode    | Data transfer time |
| -------- | ------- |  
| Normal mode      | 42.45384502410889 s   |  
| High speed mode  | 4.463783025741577 s   |

## DIGV_q_F8558.py 

Simple acquisition Fluke 8558A in voltage Digitize mode using query method

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGV_q_F8558.png)

## DIGV_F8558.py

Simple acquisition Fluke 8558A in voltage Digitize mode using query_ascii_values method

## DIGV_High_speed_F8558.py

Simple acquisition Fluke 8558A in voltage Digitize mode with high speed transfer data.

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGV_High_speed_F8558.png)


## DIGI_F8558.py

Simple acquisition Fluke 8558A in current Digitize mode using query_ascii_values method

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/DIGI_F8558.png)

## DIGI_High_speed_F8558.py

Simple acquisition Fluke 8558A in current Digitize mode with high speed transfer data.

## AC_F8558.py

Simple AC acquisition with Fluke 8558A

## DC_F8558.py

Simple DC acquisition with Fluke 8558A

## CuasiContinuos_DIGV_F8558.py

Acquire in digitize mode periodically without missing data points using a external trigger and for loop. This code not work for all combination of digitize configuration and externall trigger frecuency, below you can see a table with more information, for n_acquisition=10.  

Ext trg frec [Hz] | trg_tim [s] | trg_count [#] | python time [s] | Continuous acquisition
|--|--|--|--|--|
| 0.1 |1E-6 | 1E6 |9.97|No |
| 0.5 |1E-6 | 1E6 |5.97| No|
| 0.8 |1E-6 | 1E6 |4.96 | Yes|
| 1 |1E-6 | 1E6 |4.95 | Yes|
| 2 |1E-6 | 1E6 |4.45 | No|
| 3 |1E-6 | 1E6 |4.6 | No|
| 0.5 |1E-3 | 1E3 |1.99 | Yes |
| 0.8 |1E-3 | 1E3 |1.99 | No |
| 1 |1E-3 | 1E3 |1.99 | Yes|
| 2 |1E-3 | 1E3 |1.49 | No|

Some acquisitions

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/CuasiContinuos_DIGV_F8558.png)

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/CuasiContinuos_DIGV_F8558_t1_s1.png)

![Alt-Text](https://github.com/juliancabaleiro/pyvisa-examples/blob/main/doc/images/CuasiContinuos_DIGV_F8558_t1_0-5.png)

## Useful Links

- [Product Specifications](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8558A___pseng0700.pdf)
- [Operator Manual](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8588a____omeng0000_0.pdf)
- [Remote Programmer's Manual](https://s3.amazonaws.com/download.flukecal.com/pub/literature/8588A___rpeng0000_0.pdf)