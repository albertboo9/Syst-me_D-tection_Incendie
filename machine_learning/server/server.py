import json
import time
import numpy as np
import pandas as pd
import threading
from flask import Flask
import joblib

app = Flask(__name__)
numerical_col = ['Temperature[C]','Humidity[%]','TVOC[ppb]','eCO2[ppm]','Raw H2','Raw Ethanol','Pressure[hPa]','PM1.0','PM2.5','NC0.5','NC1.0','NC2.5']
# Charger les modèles et le scaler
model = joblib.load('machine_learning/models/randomForest.joblib')
apc = joblib.load('machine_learning/models/APC.joblib')
scaler = joblib.load('machine_learning/models/scaler.joblib')

# Fichier JSON où stocker les données
DATA_FILE = "machine_learning/server/donnee.json"

def preprocess_data(data):
    """Prétraite les données."""

    data_values = list(data.values())
    # Conversion en tableau NumPy avec précision float64
    data_array = np.array([data_values], dtype=np.float64)
    dt = pd.DataFrame(data_array, columns=numerical_col)

    datascaled = scaler.transform(dt) #on standardise les données
    
    component = apc.transform(datascaled) # on réapplique l'apc
    df = pd.DataFrame(component, columns=["Composante1","Composante2","Composante3"])

    return df

def predict_loop():
    """Boucle de prédiction en arrière-plan."""
    while True:
        try:
            # Charger les données depuis le fichier JSON
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            # Prétraitement des données
            preprocessed_data = preprocess_data(data)

            # Prédiction
            prediction = model.predict(preprocessed_data)
            if prediction == 1:
                print("Attention, un incendie a été détecté !!!!! ")
            else:
                print("relax, pas d'incendie")

        except Exception as e:
            print(f"Erreur lors de la prédiction : {e}")
        time.sleep(3)  # Ajuster le délai selon vos besoins
      

if __name__ == '__main__':
    # Lancer le thread pour les prédictions en arrière-plan
    prediction_thread = threading.Thread(target=predict_loop)
    prediction_thread.start()

    # Lancer le serveur Flask et SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)