import sys
import time
from datetime import timedelta
from flask import Flask, abort, jsonify, request, make_response, current_app
import json 
from functools import update_wrapper
from grovepi import *

app = Flask(__name__)

#CONNECTIONS
webserverIp = '0.0.0.0'

#SENSORS-OUTPUT
relay_pin = 8
buzzer = 7
button = 6
red_led = 4
ultrasound = 2

#SENSORS_INPUT
light_sensor = 2
sound_sensor = 1
temp_sensor = 0
temp_sensor_type = 0

#MATH
sound_threshold = 90
distance_threshold = 50
light_threshold = 10

#PINMODES-OUTPUT
pinMode(red_led, "OUTPUT")
pinMode(buzzer, "OUTPUT")
pinMode(relay_pin, "OUTPUT")

#PINMODES-INPUT
pinMode(sound_sensor, "INPUT")
pinMode(light_sensor, "INPUT")
pinMode(button, "INPUT")
pinMode(ultrasound, "INPUT")

#CROSSDOMAIN SHIZZLE

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#INDEX
@app.route('/')
@crossdomain(origin='*')
def index():
    return "swag"

#PANIC BUTTON
@app.route('/getButtonStatus', methods=['GET'])
@crossdomain(origin='*')
def button():
    while True:
        button_status = digitalRead(button, )
        while button_status: #while button is in HIGH mode
            try:
                digitalWrite(red_led,1)
                digitalWrite(buzzer,1)
                time.sleep(.5)

                digitalWrite(red_led,0)
                digitalWrite(buzzer,0)
                time.sleep(.5)
            except KeyboardInterrupt:
                digitalWrite(red_led,0)
                digitalWrite(buzzer,0)
                break
            except IOError:
                print "Error"

        return jsonify({'panic': button_status})

#SOUND
@app.route('/getSound', methods=['GET'])
@crossdomain(origin='*')
def getSound():
    while True:
        try:
            #get sound
            sensor_value = analogRead(sound_sensor)
            #decipher value to Decibel
            sound_value = (20 * log10(sensor_value + 1))

            #higher than threshold
            if sound_value > sound_threshold:
                digitalWrite(red_led,1)
            else:
                digitalWrite(red_led,0)

            return jsonify({'sound': sound_value})

        except IOError:
            print "Error"

#ULTRASOUND
@app.route('/getDistance', methods=['GET'])
@crossdomain(origin='*')
def getUltrasound():
    while True:
        try:
            #get distance from ultrasonic sensor to object
            distance = ultrasonicRead(ultrasound)

            if distance > distance_threshold:
                digitalWrite(red_led,1)
            else:
                digitalWrite(red_led,0)

            return jsonify({'distance': distance})

        except IOError:
            print "Error"


#LIGHT
@app.route('/getLight', methods=['GET'])
@crossdomain(origin='*')
def getLight():
    while True:
        try:
            #get sensor value
            sensor_value = analogRead(light_sensor)
            #calculate resistance lumen? i don't fcking know
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value

            if resistance > light_threshold:
                digitalWrite(red_led,1)
                return jsonify({'light': 'Light'})

            else:
                digitalWrite(red_led,0)
                return jsonify({'light': 'Dark'})

        except IOError:
            print "Error"


#TEMPERATURE
@app.route('/getTemp', methods=['GET'])
@crossdomain(origin='*')
def getTemp():
    while True:
        try:
            [ temp,hum ] = dht(temp_sensor, temp_sensor_type)
            t = str(temp)
            return jsonify({'temp': t})
        except (IOError, TypeError) as e:
            print "Error"

if __name__ = '__main__':
    app.run(debug=True,host=webserverIp)