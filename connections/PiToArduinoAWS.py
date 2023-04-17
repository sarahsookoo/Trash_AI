"""
This is the main driver code for the Pi.
Handles the connection between the arduino to Pi.
Handles the process of taking an image, processing it and running it through the model(s)
Handles the data being sent to AWS (the IoTPublish.py does this too but htat was a PoC script)
Handles sending data back to the Arduino (to move the actuator)

Essentially this is the main script thats running oon the Pi as an infinite loop. 
!!! HAS NOT BEEN TRESTED YET !!!
"""
import cv2
import numpy as np
import tensorflow as tf
from time import sleep
import serial
import paho.mqtt.client as mqtt
import ssl
import json
from datetime import datetime

# Connect Pi to arduino. Once USB is connected https://www.tomshardware.com/how-to/use-raspberry-pi-with-arduino
# What is 9600 and why (we can make this higher)? https://www.programmingelectronics.com/serial-begin-9600/. MUST be the same as arduino
def connect_to_arduino():
    arduino_serial = serial.Serial('/dev/ttyACM0', 9600) # The String could also be '/dev/ttyS0' type in dsmego in Pi to find out
    arduino_serial.reset_input_buffer()
    return arduino_serial

# Exception function handler. *args/**kwargs are to accept multiople param options for flexibility
def safely_execute_connection_function(func, *args, **kwargs):
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < 2:
                print(f"Retrying {func.__name__}... (Attempt {attempt + 1})")
    print(f"Failed to execute {func.__name__} after 3 attempts. Reason: {e}")
    return None



# Classify the image based on the model provided. 
# @param image - The image the Pi took
# @param model - The Loaded model being used
# @param is_tflite - boolean to handle additional logic for tf_lite modelse
def classify_image(image, model, is_tflite=False):
    try:
        img_resized = cv2.resize(image, (224, 224))
        img_normalized = img_resized / 255.0
        img_expanded = np.expand_dims(img_normalized, axis=0)
        if is_tflite:
            input_details = model.get_input_details()
            output_details = model.get_output_details()
            model.set_tensor(input_details[0]['index'], img_expanded)
            model.invoke()
            prediction = model.get_tensor(output_details[0]['index'])
        else:
            prediction = model.predict(img_expanded)
        return np.argmax(prediction)
    except Exception as e:
        print(f"Error predicting the class for reason: {e}")


def connectToAWS():
    client = mqtt.Client(client_id="RaspberryPi")
    # These certs were created when setting up the thing. They are saved in the raspberryPi
    ca_cert = "/home/yaya/certs/AmazonRootCA1.pem"
    client_cert = "/home/yaya/certs/5e24338b700a1626b8805c8be445981c590b0eaf20a4a5f37f0f1bf2517c417b-certificate.pem.crt"
    client_key = "/home/yaya/certs/5e24338b700a1626b8805c8be445981c590b0eaf20a4a5f37f0f1bf2517c417b-private.pem.key"
    client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    # Device Data endpoint API. Found in settings
    data_endpoint = "a3cw4o4ei9rop7-ats.iot.us-east-2.amazonaws.com"
    data_port = 8883

    # Lambda anonymous functions. Cleaner than having the callback on_connect functions
    client.on_connect = lambda responseCode: print("Connected to AWS with result code "+str(responseCode))
    client.on_message = lambda message: print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))

    client.connect(data_endpoint, data_port, keepalive=60)

    # Start the MQTT client 
    client.loop_start()
    return client


# TFLite uses a different format, to run faster on these devices. https://stackoverflow.com/questions/50443411/how-to-load-a-tflite-model-in-script
# Current saved models are 
# ['/home/yaya/mobileNetV2' , 'home/yaya/efficentNet' , '/home/yaya/vgg16']
def load_model(model_to_load):
    if model_to_load.endswith('tflite'):
        lite_interpreter = tf.lite.Interpreter(model_path=model_to_load)
        lite_interpreter.allocate_tensors()
        return lite_interpreter, True
    else:
        return tf.keras.models.load_models(model_to_load), False


# Start the connections before loop
arduino = safely_execute_connection_function(connect_to_arduino)
model_used, is_tfLite = safely_execute_connection_function(load_model, '/home/yaya/models/mobileNetV2') # Change the string path to test different models
client = safely_execute_connection_function(connectToAWS)

if arduino is None or model_used is None or client is None:
    print("Error: Connection . Exiting the program.")
    exit(1)

while True:
    try:
        weight = arduino.readline().strip()
        weight = float(weight) # Change type to integer. This is in grams

        if weight > 0:
            camera = cv2.VideoCapture(0) # Opens the camera
            ret, frame = camera.read() # ret is True/False if the camera taken was succesful
            camera.release() # Close the camera

            if ret:

                # Class index is an integer value. 0 = Plastic, 1 = Paper, 2 = Trash
                class_index = classify_image(frame, model_used, is_tfLite)
                class_label = ['plastic', 'paper', 'trash'][class_index]

                arduino.write(str(class_index).encode())
                print(f"Predicted class: {class_label}")

                # Get current date
                date = datetime.now().strftime('%Y-%m-%d')
                trash_data = {
                    "Weight": weight,
                    "Type_of_Trash": class_label,
                    "Date": date
                }
                client.publish("TrashAI", json.dumps(trash_data), qos=1)
                print(f"Sent message {json.dumps(trash_data)} to topic TrashAI")
            else:
                print("Failed to capture an image")
    except Exception as e:
            print(f"Execution failed for reason: {str(e)}")

    sleep(1)


"""
Sources
Pi to arduino AND back - https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Raspberry_Pi_Software_setup
HX711 setup (WITHOUT ARDUINO) - https://github.com/tatobari/hx711py/blob/master/example.py
Using the model to detect Images - https://stackoverflow.com/questions/50443411/how-to-load-a-tflite-model-in-script
"""