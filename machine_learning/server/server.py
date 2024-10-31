
import paho.mqtt.client as mqtt
import joblib

model = joblib.load('../models/regressionLineaire.joblib')

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        client.subscribe("home/fire_detection")
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")


def on_message(client, userdata, msg):
     print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port)
client.loop_forever()