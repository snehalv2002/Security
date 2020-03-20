import face_recognition
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import numpy as np
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

email = 'isecur29@gmail.com'
password = 'r0b1nh00d'
send_to_email = 'snehalverma10@gmail.com'
subject = 'Uh Oh'
message = 'Uh Oh!!!!'

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))


cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 16
rawCapture = PiRGBArray(cam, size=(640, 480))

time.sleep(1)

face_locations = []
names = []
frame_numbers = [0]

vimi = face_recognition.load_image_file('known/vimi.jpg')
tanmay = face_recognition.load_image_file('known/tanmay.jpg')
shreyas = face_recognition.load_image_file('known/shreyas.jpg')

vimi_encoding = face_recognition.face_encodings(vimi)[0]
tanmay_encoding = face_recognition.face_encodings(tanmay)[0]
shreyas_encoding = face_recognition.face_encodings(shreyas)[0]

known_encodings = [vimi_encoding, tanmay_encoding, shreyas_encoding]
known_names = ['vimi', 'tanmay', 'shreyas']

for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    #setup
    image = frame.array
    s_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
    rgb = s_image[:, :, ::-1]
    frame_number = 0

    i = 0
    if i % 3 == 0:
        #box setup
        face_locations = face_recognition.face_locations(rgb)[0]
        face_encodings = face_recognition.face_encodings(rgb, face_locations)[0]

        (top, right, bottom, left) = face_locations
        picture = image[top:bottom, left:right]

        matches = face_recognition.compare_faces(known_encodings, face_encodings)
        global name = "unknown"
        distances = face_recognition.face_distance(known_encodings, face_encodings)
        best_match_index = np.argmin(distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

        names.append(name)

        if "unknown" in names and frame_number - frame_numbers[-1] > 960:
            file = Image.fromarray(image)
            file.save(f"badguy{frame_number}.jpg")

            # Setup the attachment
            file_location = f'C:\\Users\\You\\Desktop\\badguy{frame_number}.jpg'
            filename = os.path.basename(file_location)
            attachment = open(file_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # Attach the attachment to the MIMEMultipart object
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string()
            server.sendmail(email, send_to_email, text)
            server.quit()
            frame_numbers.append(frame_number)

    i += 1

    top, right, bottom, left = face_locations
    bob = names[0]

    top *= 4
    right *= 4
    bottom *= 4
    left *= 4

    cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 100), 4)
    cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image, bob, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 2)

    cv2.imshow("Frame", image)
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    frame_number += 1

    if key == ord('q'):
        break
