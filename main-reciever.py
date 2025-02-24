import machine
import espnow
import network
import time
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS IS THE ESP THAT GOES INSIDE YOUR PC AND RECIEVES COMMANDS FROM THE KVM - BEFORE THAT FIND THE DEVICE MAC ADDRESS 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GPIO Outputs (connected to optocouplers, active LOW)
gpio_reboot = machine.Pin(3, machine.Pin.OUT)  # GPIO3 for Reboot
gpio_power = machine.Pin(4, machine.Pin.OUT)   # GPIO4 for Power

# Set GPIOs to default HIGH (inactive state)
gpio_reboot.value(1)  # High = inactive
gpio_power.value(1)   # High = inactive

# ESP-NOW Setup
wlan = network.WLAN(network.STA_IF)  # Station mode required for ESP-NOW
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

def process_message(message):
    """Process the received ESP-NOW message."""
    try:
        # Parse the message (assumes JSON-like format as a string)
        data = eval(message.decode('utf-8'))  # Convert the message to a dictionary
        event = data.get("event")
        state = data.get("state")
        duration = data.get("duration", 0)  # Default duration to 0 if not provided

        if event == "reboot":
            # Toggle GPIO for reboot (inverted logic)
            gpio_reboot.value(0 if state else 1)
            print(f"Reboot GPIO set to {'LOW (ON)' if state else 'HIGH (OFF)'}")

        elif event == "power":
            # Handle short and long press based on duration (inverted logic)
            if duration < 3:
                print(f"Short press detected for power button (duration: {duration}s)")
                gpio_power.value(0)  # Simulate short press (active LOW)
                time.sleep(0.1)  # 0.1-second signal
                gpio_power.value(1)  # Reset to inactive
            else:
                print(f"Long press detected for power button (duration: {duration}s)")
                gpio_power.value(0)  # Simulate long press (active LOW)
                time.sleep(duration)  # Hold GPIO for the specified duration
                gpio_power.value(1)  # Reset to inactive

    except Exception as e:
        print(f"Failed to process message: {e}")

# Main loop to listen for ESP-NOW messages
def listen_for_messages():
    print("Listening for ESP-NOW messages...")
    while True:
        peer, message = esp.recv()  # Blocking call to receive data
        if message:  # If a message is received
            print(f"Message received from {peer}: {message}")
            process_message(message)

# Start listening for messages
listen_for_messages()

