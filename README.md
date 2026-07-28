# SmartTemperatureSensor
DHT11 sensor using Arduino commands to send data towards a python script that utilizes a anthropic agent to run basic commands such as monitoring the temperature, and turning on a mini fan blade hooked up to a 130 DC motor. 

Referring to "image.jpeg" the wiring while "rudimentary" shows 2 LEDs that light based on a set temperature threshold. When the user prompts the agent to check the temperature, based on the temperature a fan is turned on automatically (RED led is turned on). There are also commands the user can give to enable or disable the fan regardless of temperature. 
