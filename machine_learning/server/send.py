#### importation des bibliothèques pour la GUI, le serceur MQTT et la creation de fichier json

import customtkinter as ctk
import json
#import paho.mqtt.client as mqtt
#import s

#création de notre fenêtre 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
log= ctk.CTk()
log.geometry("600x480")

# fonction pour recuperrer les caractères entrés au clavier
def enregistrement(temp,hum,press,co,h,eth,n0,n1):
    global donnee
    temperature = float(temp)
    humidite = float(hum)
    pression = float(press)
    co2 = float(co)
    h2 = float(h)
    ethanol = float(eth)
    nfirst = float(n0)
    nlast = float(n1)
    # on stocke tout cela dans un petit dictionnaire et après dans un fichier json 
    donnee = {
        "Temperature[C]":temperature,
        "Humidity[%]":humidite,
        "TVOC[ppb]":0,
        "eCO2[ppm]":co,
        "Raw H2":h2,
        "Raw Ethanol":ethanol,
        "Pressure[hPa]":pression,
        "PM1.0":0.06,
        "PM2.5":0.11,
        "NC0.5":nfirst,
        "NC1.0":nlast,
        "NC2.5":0.051
    }


#on doit vérifier qu'ils sont des réels avant de les enregistrés
def verify(temp,hum,press,co,h,eth,n0,n1):
    try:
        float(temp)
        float(hum)
        float(press)
        float(co)
        float(h)
        float(eth)
        float(n0)
        float(n1)
        return True
    except ValueError:
        return False
    
def connexion():
    temperature_val =temperature.get()
    humidite_val = humidite.get()
    pression_val = pression.get()
    co2_val = co2.get()
    h2_val = h2.get()
    ethanol_val = ethanol.get()
    nc0_val = nc0.get()
    nc1_val = nc1.get()
            
    if verify(temperature_val,humidite_val,pression_val,co2_val,h2_val,ethanol_val,nc0_val,nc1_val):
        #si les données sont vraiment des entiers alors on stocke dans un fichier json temporaire
        enregistrement(temperature_val,humidite_val,pression_val,co2_val,h2_val,ethanol_val,nc0_val,nc1_val)
        with open("donnee.json","w") as fichier:
            json.dump(donnee,fichier)
            
        for widget in frame1.winfo_children():
            widget.destroy()

        message=ctk.CTkLabel(frame1,text="predictions pour les donnees (température,humidité,pression,teneur en co2,volume de H2,vol ethanol,NC0 et NC1)")
        message.pack()
            
        liste =[temperature_val,humidite_val,pression_val,co2_val,h2_val,ethanol_val,nc0_val,nc1_val]
        for elt in liste :
            message1=ctk.CTkLabel(frame1,text=elt)
            message1.pack(pady=5)
        #envoi des données au serveur mqtt

        broker_address = "127.0.0.1"
        port = 8888
        user = "adruino_side"
        password = "mypassword"
        client = mqtt.client()
        client.username_pw_set(user,password)
        client.connect(broker_address,port)
        val=ctk.CTkLabel(master=frame,width=250,height=25,corner_radius=20,placeholder_text="DONNEE ENVOYEES AU SERVEUR")
        val.pack(pady=5)
    else:
        error=ctk.CTkLabel(master=frame,width=250,height=25,corner_radius=20,text="Erreur une des valeurs entrées n'est pas un nombre")
        error.pack(pady=5)

########## FONCTION POUR CHANGER DE FRAME AVEC ANIMATION
    
#########animation #################
def animation ():
    for i in range(10):
        opacity= 1-(i/10)
        frame.configure(fg_color="#333333")
        label.configure(text_color="#AAAAAA")
    frame.pack_forget()
    frame1.pack(pady=20,padx=60,fill="both",expand=True)


################ la première Frame ########################
frame=ctk.CTkFrame(master=log)
frame.pack(pady=20,padx=60,fill="both",expand=True)
label=ctk.CTkLabel(master=frame,text="SYSTEME DE DETECTION DES INCENDIES")
label.pack(pady=20,padx=10)

temperature_lab= ctk.CTkLabel(master=frame,text="temperature")
temperature_lab.pack()
temperature= ctk.CTkEntry(master=frame,width=250,height=25,corner_radius=20,placeholder_text="Entrer la valeur de la température")
temperature.pack(pady=5)

humidite_lab= ctk.CTkLabel(master=frame,text="humidite")
humidite_lab.pack()
humidite= ctk.CTkEntry(master=frame,width=250,height=25,corner_radius=20,placeholder_text="Entrer la valeur de l'humidité")
humidite.pack(pady=5)

pression_lab= ctk.CTkLabel(master=frame,text="pression")
pression_lab.pack()
pression= ctk.CTkEntry(master=frame,width=250,height=25,corner_radius=20,placeholder_text="Entrer la valeur de la pression")
pression.pack(pady=5)


co2_lab= ctk.CTkLabel(master=frame,text="teneur en CO2")
co2_lab.pack()
co2= ctk.CTkEntry(master=frame,width=250,height=25,corner_radius=20,placeholder_text="Entrer la quantité de CO2")
co2.pack(pady=5)


button=ctk.CTkButton(master=frame,width=250,height=25,corner_radius=30,text="suivant",text_color="white",command=animation)
button.pack(pady=12,padx=10)

################## Deuxiéme frame cacher ###################
frame1=ctk.CTkFrame(master=log)
frame1.pack_forget()
label=ctk.CTkLabel(master=frame1,text="PHASE FINALE D'ENVOIE DES DONNEES")
label.pack(pady=20,padx=10)

h2_lab= ctk.CTkLabel(master=frame1,text="volume de H2")
h2_lab.pack()
h2= ctk.CTkEntry(master=frame1,width=250,height=25,corner_radius=20,placeholder_text="Entrer volume d'H2")
h2.pack(pady=5)

ethanol_lab= ctk.CTkLabel(master=frame1,text="Ethanol")
ethanol_lab.pack()
ethanol= ctk.CTkEntry(master=frame1,width=250,height=25,corner_radius=20,placeholder_text="Entrer le volume d'éthanol present")
ethanol.pack(pady=5)

nc0_lab= ctk.CTkLabel(master=frame1,text="NC0")
nc0_lab.pack()
nc0= ctk.CTkEntry(master=frame1,width=250,height=25,corner_radius=20,placeholder_text="valeur NC0")
nc0.pack(pady=5)


nc1_lab= ctk.CTkLabel(master=frame1,text="NC1")
nc1_lab.pack()
nc1= ctk.CTkEntry(master=frame1,width=250,height=25,corner_radius=20,placeholder_text="valeur NC1")
nc1.pack(pady=5)


button=ctk.CTkButton(master=frame1,width=250,height=25,corner_radius=30,text="envoyer",text_color="white",command=connexion)
button.pack(pady=12,padx=10)


log.mainloop()