import machine
import espnow
import network
import time

# UART Setup
uart = machine.UART(1, baudrate=115200, tx=20, rx=21)  # Adjust TX and RX pins as needed

# ESP-NOW Setup
wlan = network.WLAN(network.STA_IF)  # Station mode required for ESP-NOW
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# Add peer (receiver's MAC address) example MAC Address: 01:4C:CA:FB:01:60 ->  b'\x01\x4C\xCA\xFB\x01\x60'
# -----------------------------------------
# code that you should use on the receiver to get mac address
# import ubinascii
# import network
# wlan_sta = network.WLAN(network.STA_IF)
# wlan_sta.active(True)
# wlan_mac = wlan_sta.config('mac')
# print(ubinascii.hexlify(wlan_mac).decode())
#014ccafb0160   <--- this will be you mac address
#-----------------------------------------
receiver_mac = b'\x01\x4C\xCA\xFB\x01\x60'  # Replace with receiver ESP32's MAC address
esp.add_peer(receiver_mac)

def send_event(event):
    """Send event data to the receiver ESP32 via ESP-NOW."""
    esp.send(receiver_mac, event)
    print(f"Sent: {event}")

def parse_uart_message(message):
    """Parse incoming UART message and return formatted event data."""
    try:
        # Expecting a format like: "event=reboot state=1 duration=0.0"
        parts = message.split()
        event = parts[0].split('=')[1]  # Extract 'event' field
        state = int(parts[1].split('=')[1])  # Extract 'state' field
        duration = float(parts[2].split('=')[1]) if len(parts) > 2 else None  # Extract 'duration' field if present

        event_data = {"event": event, "state": state}
        if duration is not None:
            event_data["duration"] = duration
        return str(event_data)
    except Exception as e:
        print(f"Failed to parse UART message: {e}")
        return None

def monitor_uart():
    """Monitor UART for incoming messages and forward them via ESP-NOW."""
    buffer = b""
    while True:
        if uart.any():
            buffer += uart.read()
            if b'\n' in buffer:  # Check for newline (end of message)
                lines = buffer.split(b'\n')
                for line in lines[:-1]:  # Process complete messages
                    message = line.decode('utf-8').strip()
                    event_data = parse_uart_message(message)
                    if event_data:
                        send_event(event_data)
                buffer = lines[-1]  # Keep the remaining incomplete message
        time.sleep(0.1)

# Start monitoring UART
monitor_uart()


