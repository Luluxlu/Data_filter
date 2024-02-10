# Fonction secondaire de chargement de fichier csv
# Types de fichiers supportés: CSV
# Date de création: 10/22/2024

# Chargement des librairies
import csv

def charge_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
    
        # Détecter les noms des champs
        headers = next(reader)

        # Création d'unne liste de dictionnaire
        data = []
    
        for row in reader:
            data.append(dict(zip(headers, row)))

    return data
