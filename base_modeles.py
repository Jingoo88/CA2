# coding: utf8
import ast
import json
import csv
from DataHandler import DataHandler

product_dict = {}
text_var = ["model", "builder", "engine", "type"]
i = 0

cr = csv.reader(open("C:/Users/Administrateur/Documents/Click&Boat/Thomas/boat24/boat24/spiders/builders.csv", "rb"))
builders = []

for row in cr:
    builders.append(row[0])

builders = [b.replace("\xe9","\u00e9") for b in builders]



with open('C:/Users/Administrateur/Documents/Click&Boat/Thomas/boat24/boat24/spiders/save.json') as data_file:
    for z in data_file:
        z = ast.literal_eval(z)
        i += 1
        z["id"] = i
        product_dict[i] = z
        if "builder" not in z.keys():

            for j in builders:
                if j in z["model"]:

                    ur = z["model"]
                    ur = ur.replace("\u00e9", "é")
                    z["builder"] = j.replace("\u00e9", "é")

                    z["builder"] = j.decode("UTF-8")

                    z["model"] = z["model"].replace(j, '')


with open('test.json') as data_file:
    data = json.load(data_file)

data_handler = DataHandler(usr=data["usr"], table=data["table"], url=data["url"], pwd=data["pwd"])


var_map = {'builder':"CONSTRUCTEUR", 'Displacement':"DEPLACEMENT", 'Beam':"MAITRE_BAU", 'Length':"LONGUEUR",
            'model':"MODELE", 'type':"TYPE",
            'No. of Beds':"CAPACITE_COUCHAGE", 'Max speed':"VITESSE_MAX", 'Range':"RANGE_NAV",
            'Engine':"MOTEUR", 'Cruising speed':"VITESSE_CROISIERE",
            'Length Waterline':"LONGUEUR_LIGNE_FLOTTAISON", 'Depth':"PROFONDEUR",
            'Certified nr. of persons':"CAPACITE_AUTORISEE", 'No. of Cabins':"NOMBRE_CABINE",
            'engine power': "PUISSANCE_MOTEUR", "id":"ID_MODELE"}

for z in product_dict.keys():

    if "Power Boat" in product_dict[z]["type"]:
        if "Rubber" in product_dict[z]["type"]:
            product_dict[z]["type"] = 4
        else:
            product_dict[z]["type"] = 2
    elif "Catamaran" in product_dict[z]["type"]:
        product_dict[z]["type"] = 3
    elif "Trimaran" in product_dict[z]["type"]:
        product_dict[z]["type"] = 3
    elif "Rubber" in product_dict[z]["type"]:
        print product_dict[z]["type"]
        product_dict[z]["type"] = 4

    else:
        product_dict[z]["type"] = 1

for z in product_dict.keys():
    for clef in product_dict[z].keys():
        if clef not in text_var:
            try:
                value = product_dict[z][clef]
                value = value.replace('m', '')
                value = value.replace('kg', '')
                value = value.replace('kn', '')
                value = value.replace('kn', '')
                value = value.strip()
                value = float(value)
                product_dict[z][clef] = value

            except:
                pass
        try:
            product_dict[z][clef] = product_dict[z][clef].replace("\r\n", " ")
            product_dict[z][clef] = product_dict[z][clef].replace("'", " ")
        except:
            pass


for key in product_dict:
    try:
        request = "UPDATE modeles SET LONGUEUR = %(type).9f WHERE ID_MODELE = %(id)i"%{"type": product_dict[key]["Length"], "id": product_dict[key]["id"]}
        data_handler.exec_request(request)
    except:
        pass
