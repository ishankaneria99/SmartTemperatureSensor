import serial
import time
import anthropic

client = anthropic.Anthropic(api_key="Ouseapihere")

tools = [
    {
        "name": "read_temperature",
        "description": "Reads the current temperature from the DHT11 sensor in Fahrenheit. Turns on the green LED if temperature is below the threshold, or the red LED if it's too high.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "enable_fan",
        "description": "Manually turns the cooling fan on at full speed",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "disable_fan",
        "description": "Manually turns the cooling fan off",
        "input_schema": {"type": "object", "properties": {}}
    }
]

arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

def send_command(cmd):
    arduino.write((cmd + '\n').encode())
    response = arduino.readline().decode().strip()
    return response

def read_temperature() -> str:
    """Reads the current temperature from the DHT11 sensor in Fahrenheit. Turns on the green LED if temperature is below the threshold, or the red LED if it's too high."""
    return send_command("READ_TEMP")

def enable_fan() -> str:
    """Turns the cooling fan on at full speed"""
    return send_command("ENABLE_FAN")

def disable_fan() -> str:
    """Turns the cooling fan off"""
    return send_command("DISABLE_FAN")

messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break

    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.content})

    for block in response.content:
        if block.type == "tool_use":
            if block.name == "read_temperature":
                result = read_temperature()
            elif block.name == "enable_fan":
                result = enable_fan()
            elif block.name == "disable_fan":
                result = disable_fan()

            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]
            })

    if response.stop_reason == "tool_use":
        final_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        print("Claude:", final_response.content[0].text)
        messages.append({"role": "assistant", "content": final_response.content})
    else:
        print("Claude:", response.content[0].text)