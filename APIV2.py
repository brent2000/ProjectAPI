#Imports van modules
import webbrowser
import sys
import requests
import base64
import json
from secrets import *
from urllib.parse import urlencode

url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

message = f"{''}:{''}"
messageBytes = message.encode('ascii')
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode('ascii')

headers['Authorization'] = f"Basic {base64Message}"
data['grant_type'] = "client_credentials"
r = requests.post(url, headers=headers, data=data)
token = r.json()['access_token']

while True:
    print("Zoek hieronder welke 10 nummers de populairste zijn van jou favoriete artiest (sterren geven populariteit weer)")
    name = ""
    #Invoer van een geldige naam
    while name == "":
        name = input("Voer de artiestennaam in: ")
        if name == "":
            print("Voer een geldige naam in")
    #Zoeken van een bijhorende artiest
    data = urlencode({"q": name, "type": "artist", "market": "BE"})
    nameFile = f"{'https://api.spotify.com/v1/search/'}?{data}"
    headers = {
        "Authorization": "Bearer " + token
    }
    resultaat1 = requests.get(url=nameFile, headers=headers)
    dataResultaat1 = resultaat1.json()
    naamArtist = dataResultaat1['artists']['items'][0]['name']
    #Gevonden artiest weergeven
    print("De 10 populairste nummers van: " + naamArtist)
    print("-------------------------------")
    #Artist uri zoeken
    artist_uri = dataResultaat1['artists']['items'][0]['uri']
    #10 top tracks van artist zoeken
    artist_uri = artist_uri[15:]
    data = urlencode({"market": "BE"})
    nameFile = f"{'https://api.spotify.com/v1/artists/' + artist_uri + '/top-tracks'}?{data}"
    headers = {
        "Authorization": "Bearer " + token
    }
    resultaat2 = requests.get(url=nameFile, headers=headers)
    dataResultaat2 = resultaat2.json()
    plaats = 0
    #10 top tracks weergeven
    for n in range(len(dataResultaat2['tracks'])):
        naamTrack = (dataResultaat2['tracks'][plaats]['name'])
        #Populariteit d.m.v. sterren
        populariteit = (int(dataResultaat2['tracks'][plaats]['popularity']))
        aantalSterren = "*"
        if populariteit <= 20:
            aantalSterren = "⭐"
        if (populariteit > 20) & (populariteit <= 40):
            aantalSterren = "⭐⭐"
        if (populariteit > 40) & (populariteit <= 60):
            aantalSterren = "⭐⭐⭐"
        if (populariteit > 60) & (populariteit <= 80):
            aantalSterren = "⭐⭐⭐⭐"
        if (populariteit > 80) & (populariteit <= 100):
            aantalSterren = "⭐⭐⭐⭐⭐"
        print(str(plaats + 1) + ". " + naamTrack + " (" +aantalSterren + ")")
        plaats = plaats + 1
    nummerkeuze = 1
    print("-------------------------------")
    #Nummer spelen, foto weergeven, stoppen, opnieuw starten
    while str(nummerkeuze) != "0":
        nummerkeuze = input("Voer het nummer in welke u wilt horen (0 = opties | foto = Foto opzoeken): ")
        if nummerkeuze == "0":
            bevestiging = "0"
            while bevestiging != 1:
                nummerkeuze2 = input("0 = Programma stoppen | 1 = Nieuwe opzoeking: ")
                #Programma stopen
                if str(nummerkeuze2) == "0":
                    print("Programma gestopt door gebruiker")
                    sys.exit()
                #Fout bij verkeerde ingave
                if str(nummerkeuze2) != "1":
                    print("Gelieve een 1 of 0 te antwoorden")
                    bevestiging = 0
                #Nieuwe opzoeking
                if str(nummerkeuze2) == "1":
                    bevestiging = 1
                    nummerkeuze = "0"
        #Foto weergeven
        if nummerkeuze.lower() == "foto":
            Foto = dataResultaat1['artists']['items'][0]['images'][0]['url']
            print("Er wordt een foto van " + naamArtist + " weergegeven in je browser.")
            #Openen browser voor tonen foto
            webbrowser.open(str(Foto), autoraise=False)
        #Nummer afspelen
        elif (nummerkeuze != "0"):
            try:
                URL = dataResultaat2['tracks'][int(int(nummerkeuze) - 1)]['external_urls']['spotify']
                if str(URL) != "None":
                    print("Nummer dat nu speelt: " + ": " + dataResultaat2['tracks'][int(int(nummerkeuze)-1)]['name'])
                    # Openen browser voor afspelen nummer
                    webbrowser.open(str(URL), autoraise=False)
                else:
                    print("Bij dit nummer kan geen audiofragment worden afgespeeld, dit ligt meestal aan de restricties die de artist oplegt")
            except:
                print("Gelieve een geldig nummer op te geven")