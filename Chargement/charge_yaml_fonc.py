# Fonction secondaire de chargement de fichier YAML
# Types de fichiers supportés: YAML
# Date de création: 10/22/2024

# Chargement des librairies
import yaml

def charge_yaml(filename):

    with open(filename, "r") as f:
        data = yaml.safe_load(f)

    return data