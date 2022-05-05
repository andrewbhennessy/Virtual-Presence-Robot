#!/usr/bin/env python
from flask import Flask, render_template, Response, request
import motor
import time
from gtts import gTTS
import os
import json

# emulated camera
#from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

app = Flask(__name__)


motorA = motor.MotorController(8,7)
motorB = motor.MotorController(10,9)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/speak_text', methods=['POST'])
def speak_text():
	text_to_speak = request.form['data']
	print("Got Message: {}".format(text_to_speak))
	myobj = gTTS(text=text_to_speak, lang='en', slow=False)
	myobj.save("text.mp3")
	os.system('mpg321 text.mp3 &')

	return "OK"


@app.route("/<direction>")
def move(direction):
	# Choose the direction of the request

	if direction =='forward':
		print("Robot Moving Forward")
		motorA.start('F',100)
		motorB.start('F',100)
		time.sleep(0.5)
		motorA.stop()
		motorB.stop()
		
	elif direction =='reverse':
		print("Robot Moving in Reverse")
		motorA.start('B',100)
		motorB.start('B',100)
		time.sleep(0.5)
		motorA.stop()
		motorB.stop()

	elif direction =='right':
		print("Robot Turning Right")
		motorA.start('B',100)
		motorB.start('F',100)
		time.sleep(0.1)
		motorA.stop()
		motorB.stop()

	elif direction =='left':
		print("Robot Turning Left")
		motorA.start('F',100)
		motorB.start('B',100)
		time.sleep(0.1)
		motorA.stop()
		motorB.stop()

		
	return direction
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', threaded=True)