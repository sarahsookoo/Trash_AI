import paho.mqtt.client as mqtt # Messaging protocol for IoT
import ssl
import json
from time import sleep

def on_connect(responseCode):
    print("Connected to AWS with result code "+str(responseCode))

def on_message(message):
    print("Received message '" + str(message.payload) + "' on topic '"
          + message.topic + "' with QoS " + str(message.qos))

# Create the Client. RaspberryPi is the "thing" name in AWS IoT
client = mqtt.Client(client_id="RaspberryPi")
client.on_connect = on_connect
client.on_message = on_message

# These certs were created when setting up the thing. They are saved in the raspberryPi
ca_cert = "/home/yaya/certs/AmazonRootCA1.pem"
client_cert = "/home/yaya/certs/5e24338b700a1626b8805c8be445981c590b0eaf20a4a5f37f0f1bf2517c417b-certificate.pem.crt"
client_key = "/home/yaya/certs/5e24338b700a1626b8805c8be445981c590b0eaf20a4a5f37f0f1bf2517c417b-private.pem.key"
client.tls_set(ca_certs=ca_cert, certfile=client_cert, keyfile=client_key, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Device Data endpoint API. Found in settings
data_endpoint = "a3cw4o4ei9rop7-ats.iot.us-east-2.amazonaws.com"
data_port = 8883
client.connect(data_endpoint, data_port, keepalive=60)

# Start the MQTT client 
client.loop_start()

"""
Just sends 10 messages to the topic.
the rule attached would then take these messages and populatew the dynamoDB
Dummy loop to get a Proof Of Concept working
"""
for i in range(10):
    trash_type = "banana peel"
    trash_name = str(i)
    payload = {"Trash": trash_name, "Type_of_Trash": trash_type}
    client.publish("TrashAI", json.dumps(payload), qos=1)
    print("Sent message " + json.dumps(payload) + " to topic TrashAI")
    sleep(5)

# Disconnect and end
client.loop_stop()
client.disconnect()
