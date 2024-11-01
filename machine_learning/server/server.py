
import paho.mqtt.client as mqtt
import joblib
import pandas as pd
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# désérialisation des composantes necessaire pour notre travail
model = joblib.load('../models/regressionLineaire.joblib')
apc = joblib.load('../models/APC.joblib')
#scaler = joblib.load('../models/scaler.joblib')
scaler = StandardScaler()

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"

def on_message(client, userdata, msg):
     print(msg.topic + " " + str(msg.payload))
     data = json.loads(msg.payload)
     datascaled = scaler.fit_transform(data)

     component  = apc.fit_transform(datascaled)
     df = pd.DataFrame(component)

     predict = model.predict(df)

     if predict == 0 :
         client.publish("home/fire_detection", "pas d'incendie 🙂‍↔️ ")
     else:
         client.publish("home/fire_detection", "il y a incendie !!! 🤯 ")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        client.subscribe("home/fire_detection")
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")

client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port)
client.loop_forever()