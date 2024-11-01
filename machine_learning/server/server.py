
import paho.mqtt.client as mqtt
import joblib
import pandas as pd
import numpy as np
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# désérialisation des composantes necessaire pour notre travail
model = joblib.load('../models/regressionLineaire.joblib')
apc = joblib.load('../models/APC.joblib')
scaler = joblib.load('../models/scaler.joblib')
#scaler = StandardScaler()

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "python_server"
password = "mypassword"
numerical_col = ['Temperature[C]','Humidity[%]','TVOC[ppb]','eCO2[ppm]','Raw H2','Raw Ethanol','Pressure[hPa]','PM1.0','PM2.5','NC0.5','NC1.0','NC2.5']

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    data = json.loads(msg.payload.decode('utf-8'))
    
    data_values = list(data.values())


    data_array = np.array([data_values], dtype=np.float64)
    df = pd.DataFrame(data_array, columns=numerical_col)
    print(df)
    datascaled = scaler.transform(df)
    component = apc.transform(datascaled).astype(np.float64)
    print(component)
    cf = pd.DataFrame(component, columns=["Composante1","Composante2","Composante3"])

    predict = model.predict(cf)

    if predict == 1 :
        client.publish("home/alarm", "Attention il y'a incendie ")
        print("incendie !!! ")
    else:
        client.publish("home/alarm", " il y a pas incendie ")
        print(" pas d'incendie ")


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