import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import json
import yaml
import xml.etree.ElementTree as ET

from src.chargement_save import charger_csv, charger_xml, charger_json, charger_yaml
from src.chargement_save import sauvegarder_xml, sauvegarder_json, sauvegarder_yaml, sauvegarder_csv


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.data_display = None
        self.save_button = None
        self.load_button = None
        self.title("Gestionnaire de Données")
        self.geometry("800x600")

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Boutons Charger et Sauvegarder
        self.load_button = tk.Button(self, text="Charger", command=self.load_data)
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self, text="Sauvegarder", command=self.save_data)
        self.save_button.pack(pady=5)

        # Zone d'affichage des données
        self.data_display = tk.Text(self, height=15, width=50)
        self.data_display.pack(pady=10)

    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Détecter le type de fichier à partir de l'extension
            extension = file_path.split('.')[-1].lower()
            if extension == 'csv':
                donnees = charger_csv(file_path)
            elif extension == 'json':
                donnees = charger_json(file_path)
            elif extension == 'xml':
                donnees = charger_xml(file_path)
            elif extension == 'yaml' or extension == 'yml':
                donnees = charger_yaml(file_path)
            else:
                messagebox.showerror("Erreur", "Type de fichier non supporté.")
                return

            # Nettoyer l'affichage avant d'ajouter les nouvelles données
            self.data_display.delete('1.0', tk.END)
            # Afficher les données
            self.data_display.insert(tk.END, str(donnees))

    def save_data(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            # Détecter le type de fichier à partir de l'extension
            extension = file_path.split('.')[-1].lower()
            # Extraire le texte de self.data_display
            donnees_texte = self.data_display.get('1.0', tk.END).strip()
            try:
                if extension in ['json', 'yaml', 'yml']:
                    if extension in ['yaml', 'yml']:
                        donnees = yaml.safe_load(donnees_texte)
                        sauvegarder_yaml(donnees, file_path)
                    else:  # JSON
                        donnees = json.loads(donnees_texte)
                        sauvegarder_json(donnees, file_path)
                elif extension == 'csv':
                    # Tente de lire le texte comme CSV pour voir s'il est correctement formaté
                    reader = csv.DictReader(donnees_texte.splitlines())
                    donnees = [row for row in reader]  # Convertir en liste pour forcer la lecture
                    entetes = donnees[0].keys() if donnees else []
                    donnees_texte = "\n".join([",".join(entetes)] + [",".join(row.values()) for row in donnees])
                    sauvegarder_csv(donnees, file_path, entetes)
                elif extension == 'xml':
                    sauvegarder_xml(donnees_texte, file_path)
                else:
                    messagebox.showerror("Erreur", "Type de fichier non supporté.")
                    return
            except Exception as e:
                messagebox.showerror("Erreur de Format",
                                     f"Les données ne sont pas au format {extension.upper()} valide.\nErreur: {str(e)}")
                return
