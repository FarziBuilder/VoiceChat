import socket
import threading
import pyaudio

def log_message(message):
    print(message)

client = socket.socket()

host = "13.201.120.248"
port = 5000

# Hard-coded values
own_value = "client3"
pair_value = "client4"

connected = False
while not connected:
    try:
        client.connect((host, port))
        client.send(f"{own_value},{pair_value}".encode())
        log_message("Connected to the server.")
        connected = True
    except Exception as e:
        log_message(f"Retrying to connect to the server: {e}")

p = pyaudio.PyAudio()

Format = pyaudio.paInt16
Chunks = 4096
Channels = 1  # Change from 2 to 1
Rate = 48000

try:
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
    log_message("Audio streams opened successfully.")
except Exception as e:
    log_message(f"Failed to open audio streams: {e}")
    exit(1)

def send():
    while True:
        try:
            data = input_stream.read(Chunks, exception_on_overflow=False)
            client.send(data)
        except Exception as e:
            log_message(f"Error in send thread: {e}")
            break

def receive():
    while True:
        try:
            data = client.recv(Chunks)
            output_stream.write(data)
        except Exception as e:
            log_value(f"Error in receive thread: {e}")
            break

t1 = threading.Thread(target=send)
t2 = threading.Thread(target=receive)

t1.start()
t2.start()

t1.join()
t2.join()

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()
client.close()

log_message("Audio streams closed and client disconnected.")
