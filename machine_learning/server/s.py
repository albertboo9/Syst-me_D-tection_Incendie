
import paho.mqtt.client as mqtt
import json

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"

variable = {
    'Temperature[C]',
    'Humidity[%]',
    'TVOC[ppb]',
    'eCO2[ppm]',
    'Raw H2',
    'Raw Ethanol',
    'Pressure[hPa]',
    'PM1.0',
    'PM2.5',
    'NC0.5',
    'NC1.0',
    'NC2.5'
}



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        data = json.dump(variable)
        client.subscribe("home/fire_detection")
        client.publish("home/fire_detection", "hello albert! ")
        client.publish("home/fire_detection", data)
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")


client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect



client.connect(broker_address, port)
client.loop_forever()