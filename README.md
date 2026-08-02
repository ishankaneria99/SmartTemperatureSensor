# SmartTemperatureSensor
DHT11 sensor using an ESP32 microcontroller to send data towards a python script that utilizes a anthropic agent to run basic commands such as monitoring the temperature, and turning on a mini fan blade hooked up to a 130 DC motor. 

Referring to "image.jpeg" the wiring while "rudimentary" shows 2 LEDs that light based on a set temperature threshold. When the user prompts the agent to check the temperature, based on the temperature a fan is turned on automatically (RED led is turned on). There are also commands the user can give to enable or disable the fan regardless of temperature. 

7/27/26 -> Created physical layout and original code where agent talks through a python shell

7/28/26 -> Utilized streamlit to create a cleaner layout to send commands to the agent

7/30/26 -> Improved layout of streamlit app

8/2/26 -> Replaced Arduino with ESP32 and included KiCad Gerber file of the circuit on a PCB (did not include fan). 
