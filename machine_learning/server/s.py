
import paho.mqtt.client as mqtt
import json

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"

variable = {
    "Temperature[C]":22.915,
    "Humidity[%]":57.07,
    "TVOC[ppb]":0,
    "eCO2[ppm]":400,
    "Raw H2":12628,
    "Raw Ethanol":19703,
    "Pressure[hPa]":939.804,
    "PM1.0":0.06,
    "PM2.5":0.11,
    "NC0.5":0.29,
    "NC1.0":0.127,
    "NC2.5":0.051
}

variable2 = {
    "Temperature[C]":-5.14,
    "Humidity[%]":50.67,
    "TVOC[ppb]":353,
    "eCO2[ppm]":400,
    "Raw H2":13075,
    "Raw Ethanol":19913,
    "Pressure[hPa]":939.281,
    "PM1.0":0.29,
    "PM2.5":0.3,
    "NC0.5":1.99,
    "NC1.0":0.311,
    "NC2.5":0.007
}



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        data = json.dumps(variable)
        #client.publish("home/fire_detection", "hello albert! ")
        client.publish("home/fire_detection", data)
        client.subscribe("home/alarm")
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")
       

def on_message(client, userdata, msg):
    print(msg.topic)

client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message



client.connect(broker_address, port)
client.loop_forever()