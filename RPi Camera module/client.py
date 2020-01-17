import io
import socket
import struct
import time
import picamera

ip = "10.0.0.73"

client_socket = socket.socket()
client_socket.connect((ip, 787))

print("Connecting..")
connection = client_socket.makefile('wb')
print("Connected, going in loop")
with picamera.PiCamera() as camera:

    print("Camera stuff")
    camera.resolution = (500, 500)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)
    
    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    
    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()

        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())

        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
                
        # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))

connection.close()
client_socket.close()
