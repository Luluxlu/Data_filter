import csv
import json
import yaml
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString



def identifier_type(valeur):
    if isinstance(valeur, bool):
        return "booléen"
    elif isinstance(valeur, int):
        return "entier"
    elif isinstance(valeur, float):
        return "réel"
    elif isinstance(valeur, str):
        return "chaîne de caractères"
    elif isinstance(valeur, list):
        types_elements = {identifier_type(elem) for elem in valeur}
        types_elements_str = ", ".join(sorted(types_elements))
        return f"liste de [{types_elements_str}]"
    else:
        return "type inconnu"


# charger un csv
def charger_csv(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        lecteur = csv.DictReader(fichier)
        lignes = [dict(ligne) for ligne in lecteur]  # Convertir chaque ligne en dictionnaire
        entetes = lecteur.fieldnames

    champs_et_types = [(entete, "chaîne de caractères") for entete in entetes]  # Simplification pour l'exemple
    return lignes, champs_et_types


# sauvegarder un csv
def sauvegarder_en_csv(donnees, chemin_fichier, entetes):
    with open(chemin_fichier, 'w', newline='', encoding='utf-8') as fichier:
        writer = csv.DictWriter(fichier, fieldnames=entetes)
        writer.writeheader()
        for item in donnees:
            # Assurez-vous que item est un dictionnaire avec les clés correspondant aux entêtes
            writer.writerow({entete: item.get(entete, '') for entete in entetes})


def extraire_champs_json(donnees):
    if isinstance(donnees, dict):
        return list(donnees.keys())
    elif isinstance(donnees, list) and donnees and isinstance(donnees[0], dict):
        return list(donnees[0].keys())
    return []


# charger un json
def charger_json(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    # Assurez-vous que donnees est une liste
    if isinstance(donnees, dict):
        donnees = [donnees]  # Mettez les données dans une liste si ce n'est pas déjà une liste

    champs_et_types = []
    if donnees:
        premier_element = donnees[0]
        champs = list(premier_element.keys()) if isinstance(premier_element, dict) else []
        champs_et_types = [(champ, identifier_type(premier_element[champ])) for champ in champs]

    return donnees, champs_et_types


# sauvegarder un json
def sauvegarder_en_json(donnees, chemin_fichier):
    with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
        # Données est une liste de dictionnaires
        json.dump(donnees, fichier, indent=4, ensure_ascii=False)


def extraire_champs_yaml(donnees):
    champs = set()
    # Parcourir chaque élément de la liste (chaque profil)
    for element in donnees:
        # Chaque élément est un dictionnaire avec un seul élément où la clé est l'identifiant du profil
        # et la valeur est le dictionnaire représentant le profil lui-même
        for profil in element.values():
            # Parcourir les champs du profil et les ajouter au set pour éviter les doublons
            champs.update(profil.keys())
    return list(champs)


# charger un yaml
def charger_yaml(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        donnees = yaml.safe_load(fichier)

    # Assurer que les données sont une liste de dictionnaires
    if not isinstance(donnees, list):
        donnees = [donnees]

    champs_et_types = []
    if donnees:
        for champ in donnees[0]:
            champs_et_types.append((champ, identifier_type(donnees[0][champ])))

    return donnees, champs_et_types


# sauvegarder un yaml
def sauvegarder_en_yaml(donnees, chemin_fichier):
    with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
        # Utilisation de allow_unicode pour gérer correctement les chaînes unicode
        yaml.dump(donnees, fichier, allow_unicode=True, default_flow_style=False)


# charger un xml
def extraire_champs_xml(element):
    champs = set()
    for sous_element in element.iter():
        champs.add(sous_element.tag)
    return list(champs)


def xml_en_dict(element):
    # Initialiser un dictionnaire vide pour le résultat
    dict_temp = {}
    # Itérer sur tous les enfants directs de l'élément donné
    for enfant in element:
        # Utiliser le tag de l'enfant comme clé
        clé = enfant.tag
        # Si l'enfant a des attributs, les ajouter comme valeur
        if enfant.attrib:
            dict_temp[clé] = enfant.attrib
        # Sinon, utiliser le texte de l'enfant comme valeur
        else:
            dict_temp[clé] = enfant.text.strip() if enfant.text else ""
    return dict_temp


def charger_xml(chemin_fichier):
    arbre = ET.parse(chemin_fichier)
    racine = arbre.getroot()
    # Créer une liste de dictionnaires pour chaque enfant direct de la racine
    donnees = [xml_en_dict(enfant) for enfant in racine]
    # Extraire les champs à partir des clés du premier dictionnaire (si les données ne sont pas vides)
    champs = list(donnees[0].keys()) if donnees else []
    champs_et_types = [(champ, "Données XML") for champ in champs]  # Simplification pour l'exemple

    return donnees, champs_et_types


# sauvegarder un xml
def sauvegarder_en_xml(donnees, chemin_fichier, entetes):
    racine = ET.Element('Root')
    for item in donnees:
        item_element = ET.SubElement(racine, 'Item')
        for entete in entetes:
            child = ET.SubElement(item_element, entete)
            # Supposons que chaque item est un dictionnaire où la clé est l'entête
            child.text = str(item.get(entete, ""))

    # Construire l'arbre XML et convertir en chaîne
    rough_string = ET.tostring(racine, 'utf-8')
    reparsed = parseString(rough_string)

    # Écrire le joli formatage dans le fichier
    with open(chemin_fichier, 'w', encoding='utf-8') as fichier:
        # prettyxml renvoie une chaîne formatée avec des indentations pour chaque élément
        fichier.write(reparsed.toprettyxml(indent="  "))


