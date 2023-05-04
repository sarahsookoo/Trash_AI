"""
This is the main driver code for the Pi.
Handles the connection between the arduino to Pi.
Handles the process of taking an image, processing it and running it through the model(s)
Handles the data being sent to AWS (the IoTPublish.py does this too but htat was a PoC script)
Handles sending data back to the Arduino (to move the actuator)

Essentially this is the main script thats running oon the Pi as an infinite loop. 
!!! HAS NOT BEEN TRESTED YET !!!
"""

import tensorflow as tf
from time import sleep
import serial
import paho.mqtt.client as mqtt
import ssl
import json
from datetime import datetime
import cv2
import numpy as np
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg16
from keras.applications.mobilenet_v2 import preprocess_input as preprocess_input_mobilenetv2
from keras.applications.efficientnet import preprocess_input as preprocess_input_efficientnet
from keras.models import load_model


def connect_to_arduino():
    """
    Connects the Raspberry Pi to an Arduino through a serial port. 9600 is the baud rate, rate of data communication between serial communication.

    Returns:
        serial.Serial: The serial connection object for the Arduino.
    """
    arduino_serial = serial.Serial('/dev/ttyACM0', 9600)
    arduino_serial.reset_input_buffer()
    return arduino_serial

def read_weight_from_arduino(arduino_serial):
    if arduino_serial.inWaiting() > 0:
        data = arduino_serial.readline().decode().strip()
        return float(data)
    else:
        return None
    

def safely_execute_connection_function(func, *args, **kwargs):
    """
    Executes a connection function safely by retrying up to three times if an exception occurs.

    Args:
        func (the_function): The connection function to execute.
        *args: Variable length argument list for `func`.
        **kwargs: Arbitrary keyword arguments for `func`.

    Returns:
        Any: The result of `func` or None if `func` fails after three attempts.
    """
    for attempt in range(3):
        try:
            result = func(*args, **kwargs)
            return result
            
        except Exception as e:
            if attempt < 2:
                print(f"Retrying {func.__name__}... (Attempt number {attempt + 1})")
            else:
                print(f"Failed running {func.__name__} after 3 attempts. ERROR: {e}")
                return None



def classify_image(image, model, model_name, is_tflite=False):
    """
    Classifies an image based on a loaded model.

    Args:
        image (numpy.ndarray): The image to classify.
        model (tf.keras.models.Model | tf.lite.Interpreter): The loaded model to use for classification.
        model_name (str): The name of the loaded model.
        is_tflite (bool): True if the model is a TFLite model; False if not.

    Returns:
        int: The index of the predicted class. [0,1,2]
    """
    try:
        img_resized = cv2.resize(image, (224, 224))
        img_array = img_resized.astype('float32') # Neural networks work with floating point numbers
        
        if model_name == 'vgg16':
            img_preprocessed = preprocess_input_vgg16(img_array) # VGG16 subtracts the mean RGB values
        elif model_name == 'mobilenetv2':
            img_preprocessed = preprocess_input_mobilenetv2(img_array) # Changes the pixel values from the range [0, 255] to the range [-1, 1]
        elif model_name == 'efficientnet':
            img_preprocessed = preprocess_input_efficientnet(img_array) # Changes the pixel values from the range [0, 255] to the range [-1, 1]
        else:
            raise ValueError("Invalid model_name.")
        
        img_expanded = np.expand_dims(img_preprocessed, axis=0) # Keras Conv layers expect a 4D format. This adds a default batch layer of 1
        
        if is_tflite:
            input_details = model.get_input_details()
            output_details = model.get_output_details()
            model.set_tensor(input_details[0]['index'], img_expanded)
            model.invoke()
            prediction = model.get_tensor(output_details[0]['index'])
        else:
            
            model_from_tuple = model[0]
            
            prediction = model_from_tuple.predict(img_expanded)
        
        return np.argmax(prediction)
    except Exception as e:
        print(f"Error predicting the class: {e}")


def connect_to_aws():
    """
    Connects the Raspberry Pi to AWS IoT.

    Returns:
        paho.mqtt.client.Client: The MQTT (Message Queuing Telemetry Transport) client object for the connection. Communicates by subscribing to topics for messages.
    """

    client = mqtt.Client(client_id="RaspberryPi")

    # Load the certificate files for the connection
    ca_cert = "/home/yaya/certs/AmazonRootCA1.pem"
    client_cert = "/home/yaya/certs/5e24338b700a1626b8805c8be445981c590b0eaf20a4a5f37f0f1bf2517c417b-certificate.pem.crt"
    client_key = "/home/yaya/certs/aa35ed2c5af8104858409803d3d1eef7b8e7cc9d912b71df328b1b6a6f09b305-private.pem.key"
    client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    
    # Set up the connection parameters
    data_endpoint = "a3cw4o4ei9rop7-ats.iot.us-east-2.amazonaws.com"
    data_port = 8883
    
    # Lambda anonymous functions. Cleaner than having the callback on_connect functions
   # client.on_connect = lambda responseCode: print("Connected to AWS with result code "+str(responseCode))
  #  client.on_message = lambda message: print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))

    # Connect the client to the endpoint
    client.connect(data_endpoint, data_port, keepalive=60)
    print("Connected to AWS!")
    # Start the MQTT client 
    client.loop_start()
    return client


def load_local_model(model_to_load):
    """
    Loads a trained model.

    Args:
        model_to_load (str): The file path of the model.

    Returns:
        tuple: A tuple containing the loaded model and a boolean indicating if the model is a TFLite model.
    """
    if model_to_load.endswith('tflite'): 
        lite_interpreter = tf.lite.Interpreter(model_path=model_to_load)
        lite_interpreter.allocate_tensors()
        print("Model loaded")
        return lite_interpreter, True
    else:
        return load_model(model_to_load), False

# Start the connections before loop
model = load_local_model('/home/yaya/Projects/Trash_AI/models/mobileNetV2.h5')
arduino = safely_execute_connection_function(connect_to_arduino)
client = safely_execute_connection_function(connect_to_aws)
print("All connections succesfful!")
if model is None or client is None:
    print("Error: Connection. Exiting the program.")
    exit(1)

while True:
    try:
        weight = read_weight_from_arduino(arduino_serial=arduino)
        print("The weiht from the Arduino is:", weight)

        if weight is not None:
            camera = cv2.VideoCapture(0)
            picture_taken, picture = camera.read()
            camera.release()       

            if picture_taken:
                print('Picture taken')
                # Class index is an integer value. 0 = Plastic, 1 = Paper, 2 = Trash
                class_index = classify_image(picture, model, "mobilenetv2", False) # This MUST match the path of model used
                class_label = ['plastic', 'paper', 'trash'][class_index]

                arduino.write(str(class_index).encode())
                print(f"Predicted class: {class_label}")

                # Get current date
                date = datetime.now().strftime('%m-%d-%Y')
                trash_data = {
                    "Type_of_Trash": class_label,
                    "Weight": weight,
                    "Date": date
                }
                
                client.publish("TrashAI", json.dumps(trash_data), qos=1)
                print(f"Sent message {json.dumps(trash_data)} to topic TrashAI")
                
            else:
                print("Failed to capture an image")
    except Exception as e:
            print(f"Execution failed for reason: {str(e)}")

    sleep(10000)


"""
Sources
Pi with Arduino USB: https://www.tomshardware.com/how-to/use-raspberry-pi-with-arduino
What is 9600 and why? https://www.programmingelectronics.com/serial-begin-9600/.
Pi to arduino AND back - https://roboticsbackend.com/raspberry-pi-arduino-serial-communication/#Raspberry_Pi_Software_setup
HX711 setup (WITHOUT ARDUINO) - https://github.com/tatobari/hx711py/blob/master/example.py
Using the model to detect Images - https://stackoverflow.com/questions/50443411/how-to-load-a-tflite-model-in-script
Image preprocessing - https://stackoverflow.com/questions/66426381/what-is-the-use-of-expand-dims-in-image-processing
"""