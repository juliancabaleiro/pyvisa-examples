# Dash Examples

Here you can find simple examples of how to use graphical interface **dash** to perform measurements with **PyVISA**. To do this you need to use a subprocess to control the instrument and communicate this with dash. To learn more about multirpocessing, I recommend read [Super Fast python-Multiprocessing Guide](https://superfastpython.com/multiprocessing-in-python/).   
For more example of **dash**  and multirpocessing in measurement application can see the folders multiproccessing and dash in [nidaqmx-python-examples](https://github.com/juliancabaleiro/nidaqmx-python-examples/tree/main/examples).

## How to launch a Dash app

Only run the desired python file and open the local host printed in the terminal in your internet browser and can interact with the app.  
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

## dash_LiveUpdate_HP34401.py

This code show a simple example to how perform a simple AC measurement with HP34401 and show this in live update plot in dash app.

![Alt Text](https://github.com/juliancabaleiro/pyvisa-examples/doc/images/dash_LiveUpdate_HP34401.gif)




