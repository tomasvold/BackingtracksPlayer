# MockGPIOClass.py
# This module simulates the RPi.GPIO library for development on a PC

# Define constants
BCM = 11
OUT = 1
HIGH = 1
LOW = 0

# A simple dictionary to hold the state of our mock pins
pins = {}

# Mock functions to simulate GPIO methods
def setmode(mode):
    print(f"MockGPIO: Set mode to {mode}")

def setup(channel, direction):
    print(f"MockGPIO: Setting up channel {channel} as {'OUT' if direction == OUT else 'IN'}")
    pins[channel] = LOW

def output(channel, value):
    print(f"MockGPIO: Setting channel {channel} to {'HIGH' if value == HIGH else 'LOW'}")
    pins[channel] = value

def cleanup():
    print("MockGPIO: Cleaning up GPIO")