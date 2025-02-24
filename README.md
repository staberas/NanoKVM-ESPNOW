# NanoKVM-ESPNOW![ESPNOW - KVM- 2](https://github.com/user-attachments/assets/d24a88ca-6285-45cf-bb32-3b819c7f29ab)


gpio-monitor.sh must run the esp32's to work and know the nanokvm shutdown/reboot actions

Use the following command to run in the background: 
./gpio-monitor.sh &
(this will work until the nanokvm loses power or resets)

---------------------------------------------------
##
Explanation of the Shell Script
-------------
**GPIO Monitoring:**

The script monitors the states of the GPIOs /sys/class/gpio/gpio505/value (reboot) and /sys/class/gpio/gpio503/value (power).

**UART Communication:**

Sends messages over the specified UART device (/dev/ttyS1).
Messages follow the format:
`
event=<event_name> state=<state_value> duration=<duration_value>
`

Example for a short press: event=power state=0 duration=1
Example for a reboot: event=reboot state=1 duration=0.0

Press Duration Calculation:

For the power button, the script calculates the duration between press and release (state=1 to state=0).

**Non-Blocking:**

The script runs in an infinite loop but does not block the system. It checks GPIOs every 0.1 seconds.

##
Testing the System
------------
**LicheeRV Nano:**

Deploy the shell script (gpio_monitor.sh) on the Nano.
Run it: sh gpio_monitor.sh.
Verify that it sends messages over the UART interface when GPIO states change.

---------------

**ESP32 Transmitter:**

Connect the UART RX/TX lines to the Nano.
Run the corrected ESP32 transmitter script.
Monitor its UART logs to confirm it parses and forwards the messages via ESP-NOW.

--------------------

**ESP32 Receiver:**

Ensure the ESP32 receiver script is running and handling the forwarded messages correctly (e.g., toggling GPIOs connected to optocouplers).
