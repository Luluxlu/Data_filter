# Fonciton de détection du format de fichier
# Date de création: 10/22/2024


def type_fichier(filename):
    extension = filename.split(".")[-1]

    if extension in {"csv"}:
        return "csv"
    elif extension in {"json"}:
        return "json"
    elif extension in {"xml"}:
        return "xml"
    elif extension in {"yaml", "yml"}:
        return "yaml"
    else:
        raise ValueError(f"Format de fichier non supporté : {extension}")