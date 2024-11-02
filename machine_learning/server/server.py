import paho.mqtt.client as mqtt
import joblib
import decimal
import pandas as pd
import numpy as np
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Désérialisation des modèles
model = joblib.load('../models/regressionLineaire.joblib')
apc = joblib.load('../models/APC.joblib')
scaler = joblib.load('../models/scaler.joblib')

# Paramètres de connexion MQTT
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"
numerical_col = ['Temperature[C]','Humidity[%]','TVOC[ppb]','eCO2[ppm]','Raw H2','Raw Ethanol','Pressure[hPa]','PM1.0','PM2.5','NC0.5','NC1.0','NC2.5']

def on_message(client, userdata, msg):
    # Décodage du message MQTT
    data = json.loads(msg.payload.decode('utf-8'))
    data_values = list(data.values())
    

    # Conversion en tableau NumPy avec précision float64
    data_array = np.array([data_values], dtype=np.float64)
    dt = pd.DataFrame(data_array, columns=numerical_col)
    # Standardisation (suppose que le scaler a été entraîné sur des données float64)
    data_scaled = scaler.transform(dt)

    # Application de l'ACP
    component = apc.transform(data_scaled)

    # Arrondi à 16 chiffres après la virgule
    component_rounded = np.round(component, 16)
 
    df = pd.DataFrame(component_rounded, columns=["Composante1","Composante2","Composante3"])

    df.to_csv('../data/temp/component.csv', index=False)

    cf = pd.read_csv('../data/temp/component.csv')
   
    # Prédiction
    predict = model.predict(cf[:1])
    print

    # Publication du résultat
    if predict > 0.6 :
        client.publish("home/alarm", "Attention il y'a incendie ")
        print("incendie !!!! ")
    else:
        client.publish("home/alarm", " il y a pas d'incendie ")
        print("il ya pas un incendie !")


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