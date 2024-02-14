# Fonction secondaire de chargement de fichier xml
# Types de fichiers supportés: XML
# Date de création: 10/022/2024

# Chargement des librairies
import xml.etree.ElementTree as ET

def charge_xml(filename):
    
    with open(filename, "r") as f:
        tree = ET.parse(f)
        root = tree.getroot()

    
    data = []
    for element in root:
        data.append(dict(zip([e.tag for e in element], [e.text for e in element])))

    return data