#!/bin/sh

# GPIO paths (adjust these paths as per your LicheeRV configuration)
GPIO_REBOOT="/sys/class/gpio/gpio505/value"
GPIO_POWER="/sys/class/gpio/gpio503/value"

# UART device (replace with the correct UART interface for LicheeRV Nano)
UART_DEVICE="/dev/ttyS1"
BAUD_RATE="115200"

# Initialize UART
stty -F $UART_DEVICE $BAUD_RATE cs8 -cstopb -parenb

# State tracking
LAST_REBOOT=0
LAST_POWER=0

# Monitor GPIOs and send events over UART
while true; do
    CURRENT_REBOOT=$(cat $GPIO_REBOOT)
    CURRENT_POWER=$(cat $GPIO_POWER)

    # Detect reboot button state change
    if [ "$CURRENT_REBOOT" -ne "$LAST_REBOOT" ]; then
        echo "event=reboot state=$CURRENT_REBOOT duration=0.0" > $UART_DEVICE
        LAST_REBOOT=$CURRENT_REBOOT
    fi

    # Detect power button state change
    if [ "$CURRENT_POWER" -ne "$LAST_POWER" ]; then
        # Long press handling
        if [ "$CURRENT_POWER" -eq 1 ]; then
            POWER_PRESS_START=$(date +%s)
        else
            POWER_PRESS_END=$(date +%s)
            PRESS_DURATION=$((POWER_PRESS_END - POWER_PRESS_START))
            echo "event=power state=0 duration=$PRESS_DURATION" > $UART_DEVICE
        fi
        LAST_POWER=$CURRENT_POWER
    fi

    sleep 0.1
done
