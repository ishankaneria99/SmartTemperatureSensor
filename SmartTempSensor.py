import streamlit as st
import serial
import time
import anthropic

# --- Setup (runs once) ---
if "client" not in st.session_state:
    st.session_state.client = anthropic.Anthropic(api_key="bleh")
    st.session_state.arduino = serial.Serial('COM3', 9600, timeout=3)
    time.sleep(2)
    st.session_state.messages = []

client = st.session_state.client
arduino = st.session_state.arduino

tools = [
    {"name": "read_temperature", "description": "Reads the current temperature from the Arduino's DHT11 sensor in Fahrenheit. Also automatically turns on the green LED if temperature is normal, or the red LED if it's too high.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "enable_fan", "description": "Manually turns the cooling fan on at full speed.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "disable_fan", "description": "Manually turns the cooling fan off.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "turn_on_green", "description": "Turns on the green LED.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "turn_on_red", "description": "Turns on the red LED.", "input_schema": {"type": "object", "properties": {}}},
    {"name": "change_fan_dir", "description": "Switches the direction the fan motor spins.", "input_schema": {"type": "object", "properties": {}}}
]

def send_command(cmd):
    print(f"[DEBUG] Sending command: {repr(cmd)}")   
    arduino.write((cmd + '\n').encode())
    return arduino.readline().decode().strip()

def read_temperature(): return send_command("read_temp")
def enable_fan(): return send_command("enable_fan")
def disable_fan(): return send_command("disable_fan")
def turn_on_green(): return send_command("turn_on_green")
def turn_on_red(): return send_command("turn_on_red")
def change_fan_dir(): return send_command("change_fan_dir")

st.title("🌡️ Smart Temp Sensor Agent")

# Display past messages
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant") and isinstance(msg["content"], str):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Chat input box
user_input = st.chat_input("Ask about the temperature or control the fan...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=st.session_state.messages
    )

    st.session_state.messages.append({"role": "assistant", "content": response.content})

    for block in response.content:
        if block.type == "tool_use":
            if block.name == "read_temperature":
                result = read_temperature()
                print(f"[DEBUG] Raw result: {repr(result)}")
            elif block.name == "enable_fan":
                result = enable_fan()
            elif block.name == "disable_fan":
                result = disable_fan()
            elif block.name == "turn_on_green":
                result = turn_on_green()
            elif block.name == "turn_on_red":
                result = turn_on_red()
            elif block.name == "change_fan_dir":
                result = change_fan_dir()

            st.session_state.messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]
            })

    if response.stop_reason == "tool_use":
        final_response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=st.session_state.messages
        )
        answer = final_response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        answer = response.content[0].text

    with st.chat_message("assistant"):
        st.write(answer)
        print("Claude:", final_response.content[0].text)
        messages.append({"role": "assistant", "content": final_response.content})
    else:
        print("Claude:", response.content[0].text)
