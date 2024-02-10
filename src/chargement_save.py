import csv
import json
import yaml
import xml.etree.ElementTree as ET


# charger un csv
def charger_csv(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        lecteur = csv.DictReader(fichier)
        lignes = [ligne for ligne in lecteur]

    # Convertir en chaîne formatée
    if not lignes:
        return "Aucune donnée trouvée."

    entetes = lignes[0].keys()
    lignes_formattees = [",".join(entetes)]  # Ajouter les en-têtes
    for ligne in lignes:
        valeurs = [str(ligne[entete]) for entete in entetes]
        lignes_formattees.append(",".join(valeurs))

    return "\n".join(lignes_formattees)


# sauvegarder un csv
def sauvegarder_csv(donnees, chemin_fichier, entetes):
    with open(chemin_fichier, mode='w', encoding='utf-8', newline='') as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=entetes)
        ecrivain.writeheader()
        ecrivain.writerows(donnees)


# charger un json
def charger_json(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)
    return json.dumps(donnees, indent=4, ensure_ascii=False)


# sauvegarder un json
def sauvegarder_json(donnees, chemin_fichier):
    with open(chemin_fichier, mode='w', encoding='utf-8') as fichier:
        json.dump(donnees, fichier, indent=4)


# charger un xml
def afficher_xml(element, niveau=0):
    indentation = '    ' * niveau
    # Préparer la chaîne de caractères pour les attributs de la balise
    attributs = ' '.join([f'{k}="{v}"' for k, v in element.attrib.items()]).strip()
    attributs = f" {attributs}" if attributs else ""

    # Ouvrir la balise avec ses attributs
    ouverture_balise = f"<{element.tag}{attributs}>"
    result = f"{indentation}{ouverture_balise}"

    # Vérifier si l'élément contient du texte, des sous-éléments, ou les deux
    if element.text and element.text.strip():
        # Ajouter le texte de l'élément directement après la balise ouverte
        result += element.text.strip()
    if list(element):  # Si l'élément a des sous-éléments, les traiter récursivement
        result += "\n"
        for sous_element in element:
            result += afficher_xml(sous_element, niveau + 1)
        result += indentation  # Ajouter l'indentation pour la balise de fermeture
    elif element.text and element.text.strip():
        # Si l'élément contient du texte mais pas de sous-éléments, fermer la balise sur la même ligne
        pass
    else:
        # Si l'élément n'a ni texte ni sous-éléments, ajouter un retour à la ligne après l'ouverture de la balise
        result += "\n"

    # Ajouter la balise de fermeture
    fermeture_balise = f"</{element.tag}>"
    result += f"{fermeture_balise}\n"

    return result


def charger_xml(chemin_fichier):
    arbre = ET.parse(chemin_fichier)
    racine = arbre.getroot()
    donnees = afficher_xml(racine)
    return donnees


# sauvegarder un xml
def sauvegarder_xml(donnees, chemin_fichier):
    try:
        # Parser le texte XML en un objet ElementTree
        racine = ET.fromstring(donnees)
        arbre = ET.ElementTree(racine)
        # Sauvegarder l'arbre XML dans un fichier
        arbre.write(chemin_fichier, encoding="utf-8", xml_declaration=True)
    except ET.ParseError as e:
        raise ValueError(f"Erreur lors du parsing XML: {e}")


# charger un yaml
def charger_yaml(chemin_fichier):
    with open(chemin_fichier, mode='r', encoding='utf-8') as fichier:
        donnees = yaml.safe_load(fichier)
    return yaml.dump(donnees, allow_unicode=True, default_flow_style=False, indent=4)


# sauvegarder un yaml
def sauvegarder_yaml(donnees, chemin_fichier):
    with open(chemin_fichier, mode='w', encoding='utf-8') as fichier:
        yaml.safe_dump(donnees, fichier, allow_unicode=True)
