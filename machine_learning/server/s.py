
import paho.mqtt.client as mqtt

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        client.subscribe("home/fire_detection")
        client.publish("home/fire_detection", "hello albert! ")
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")


client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect



client.connect(broker_address, port)
client.loop_forever()