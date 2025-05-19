#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

LED_EN_PIN = 17  # BCM numbering

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_EN_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_EN_PIN, GPIO.HIGH)
        print("PIN HIGH")
        time.sleep(1)
        GPIO.output(LED_EN_PIN, GPIO.LOW)
        print("PIN LOW")
        time.sleep(1)
finally:
    GPIO.cleanup()
