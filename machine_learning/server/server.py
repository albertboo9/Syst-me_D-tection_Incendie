import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        client.subscribe("home/fire_detection")  # S'abonner au topic
    else:
        print("Échec de la connexion (code de retour " + str(rc) + ")")

def on_message(client, userdata, msg):
    print(f"Message reçu sur le topic {msg.topic}: {str(msg.payload.decode('utf-8'))}")  # Décoder le payload en UTF-8

broker_address = "votre_adresse_ip"
port = 8888

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port, 60)

client.loop_forever()