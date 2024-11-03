
import paho.mqtt.client as mqtt
import json
#import smtplib 

#configuration de l'envoie des mail

#host = "localhost"
#port = 5555

#smtpOBJ = smtplib.SMTP([host])

# Paramètres de connexion
broker_address = "127.0.0.1"
port = 8888
user = "arduino_side"
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
c = {17.242, 53.71, 1117,400,12911,19452,938.702,1.63,1.7,11.25,1.754,0.04}
variable2 = {
    "Temperature[C]":14.901369,
    "Humidity[%]":51.367693,
    "TVOC[ppb]":810.682730,
    "eCO2[ppm]":405.007016,
    "Raw H2": 13025.023771,
    "Raw Ethanol":20269.400985,
    "Pressure[hPa]":938.676613,
    "PM1.0":1.193409,
    "PM2.5":1.241376,
    "NC0.5":8.210595,
    "NC1.0":1.282602,
    "NC2.5":0.030301
}

def on_message(client, userdata, msg):
    print(msg.topic + " = " + msg.payload.decode('utf-8'))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT avec succès !")
        data = json.dumps(variable2)
        #client.publish("home/fire_detection", "hello albert! ")
        client.publish("home/fire_detection", data)
        client.subscribe("house/alarm")
    else:
        print(f"Échec de la connexion (code de retour {str(rc)})")
       
#def email(mail, message):



client = mqtt.Client()
client.username_pw_set(user, password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port)
client.loop_forever()