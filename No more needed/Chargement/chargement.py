# Fonction de chargement de fichier
# Types de fichiers supportés: CSV, SON, XML, YAML
# Date de création: 10/22/2024

# Importation des fonctions
from type_fhichier_fonc import type_fichier
from charge_csv_fonc import charge_csv
from charge_json_fonc import charge_json
from charge_xml_fonc import charge_xml
from charge_yaml_fonc import charge_yaml


def chargement(filename):

    # On détermine le type du fichier
    type = type_fichier(filename)

    # Chargement des fichiers
    if type == "csv":
        data = charge_csv(filename)

    elif type == "json":
        data = charge_json(filename)

    elif type == "xml":
        data = charge_xml(filename)

    elif type == "yaml":
        data = charge_yaml(filename)

    else:
        print("Le fichier inséré n'est pas supporté")

    return data
    