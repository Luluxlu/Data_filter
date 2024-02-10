# Fonction secondaire de chargement de fichier json
# Types de fichiers supportés: JSON
# Date de création: 10/22/2024

# Chargement des librairies
import json

def charge_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    return data