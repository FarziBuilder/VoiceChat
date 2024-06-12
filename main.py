import socket
import threading
import pyaudio
import RPi.GPIO as GPIO
import time

# Setup GPIO for button
GPIO.setmode(GPIO.BCM)
button_pin = 2
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

client = socket.socket()

host = "13.201.120.248"  # or "211.255.212.196"
port = 5000

# Hard-coded values
own_value = "client1" #RPI 1
pair_value = "client2"

connected = False
while not connected:
    try:
        client.connect((host, port))
        client.send(f"{own_value},{pair_value}".encode())
        print("Connected to the server.")
        connected = True
    except socket.error as e:
        print(f"Connection failed, retrying: {e}")
        time.sleep(1)  # wait a bit before retrying to avoid flooding the network

p = pyaudio.PyAudio()

Format = pyaudio.paInt16
Chunks = 4096
Channels = 1   # Change from 2 to 1
Rate = 48000   # Match the rate with the first code

input_stream = p.open(format=Format,
                      channels=Channels,
                      rate=Rate,
                      input=True,
                      frames_per_buffer=Chunks)

output_stream = p.open(format=Format,
                       channels=Channels,
                       rate=Rate,
                       output=True,
                       frames_per_buffer=Chunks)

def send():
    while True:
        try:
            button_state = GPIO.input(button_pin)
            if button_state == GPIO.LOW:  # Button is pressed
                data = input_stream.read(Chunks, exception_on_overflow=False)
                client.send(data)
            else:
                time.sleep(0.01)  # Reduce sleep time to lower latency
        except IOError as e:
            if e.errno == pyaudio.paInputOverflowed:
                print("Input overflowed")
                continue
            else:
                print(f"Send error: {e}")
                break

def receive():
    while True:
        try:
            data = client.recv(Chunks)
            output_stream.write(data)
        except Exception as e:
            print(f"Receive error: {e}")
            break

t1 = threading.Thread(target=send)
t2 = threading.Thread(target=receive)  # Corrected this line

t1.start()
t2.start()

t1.join()
t2.join()

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()

GPIO.cleanup()
