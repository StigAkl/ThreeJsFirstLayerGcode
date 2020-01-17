import socket
import numpy as np 
import cv2
import io
import struct 

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 787))

print("Listening")
server_socket.listen(0)
# Accept a single connection and make a file-like object out of it

print("Accepting..")
conn = server_socket.accept()[0]
print("Accepted")
print("Connecting..")
connection = conn.makefile('rb')

print("Connected")
while True:

    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
    if not image_len:
        print("no image len..")
        break

    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    image_stream.seek(0)

    data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
    frame = cv2.imdecode(data, 1)


    # Set minimum and max HSV values to display
    lower = np.array([63, 73, 0])
    upper = np.array([97, 143, 255])

    #Cropping region
    maxHorizontal = 350
    minHorizontal = 60
    minVertical = 210
    maxVertical = 430

    roi = frame[minVertical:maxVertical, minHorizontal:maxHorizontal]


    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)


    kernel = np.ones((5,5),np.float32)/25
    mask = cv2.filter2D(mask, -1, kernel)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    output = cv2.bitwise_and(roi,roi, mask= mask)

    x, y, w, h = cv2.boundingRect(cnts[0])

    cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0), 1)
    #cv2.rectangle(frame, (x+minVertical, y+minHorizontal), (x+w+maxHorizontal, y+h+maxVertical), (0, 255, 0), 1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", output)
    cv2.waitKey(1)


    ## HSV: (175, 108, 124) to (179, 190, 204)