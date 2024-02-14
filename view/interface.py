import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import json
import yaml
import xml.etree.ElementTree as ET

from src.chargement_save import charger_csv, charger_xml, charger_json, charger_yaml
from src.chargement_save import sauvegarder_en_xml, sauvegarder_en_json, sauvegarder_en_yaml, sauvegarder_en_csv

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de Données")
        self.geometry("800x600")
        self.donnees_avec_types = []
        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self, text="Charger", command=self.load_data)
        self.load_button.pack(pady=5)

        self.save_button = tk.Button(self, text="Sauvegarder", command=self.save_data)
        self.save_button.pack(pady=5)

        self.stats_button = tk.Button(self, text="Calculer Statistiques", command=self.calculate_and_display_stats)
        self.stats_button.pack(pady=5)

        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill='both', pady=10)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.champs_combobox = ttk.Combobox(self, state="readonly", width=60)
        self.champs_combobox.pack(pady=5)

    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            extension = file_path.split('.')[-1].lower()
            donnees_formattees, champs = [], []
            if extension == 'csv':
                donnees_formattees, champs = charger_csv(file_path)
            elif extension == 'json':
                donnees_formattees, champs = charger_json(file_path)
            elif extension == 'xml':
                donnees_formattees, champs = charger_xml(file_path)
            elif extension == 'yaml' or extension == 'yml':
                donnees_formattees, champs = charger_yaml(file_path)
            else:
                messagebox.showerror("Erreur", "Type de fichier non supporté.")
                return

            self.update_combobox(champs)
            champs = [champ for champ, _ in champs]
            self.donnees_avec_types = donnees_formattees
            self.update_treeview(champs, donnees_formattees)

    def save_data(self):
        # La logique pour sauvegarder les données va ici.
        pass

    def calculate_and_display_stats(self):
        stats = self.calculate_stats(self.donnees_avec_types)
        self.display_stats(stats)

    def calculate_stats(self, donnees):
        stats = {}
        for donnee in donnees:
            for champ, valeur_str in donnee.items():
                valeur = self.parse_value(valeur_str)
                # Gestion des valeurs numériques
                if isinstance(valeur, float):
                    if champ not in stats:
                        stats[champ] = {'min': valeur, 'max': valeur, 'somme': valeur, 'count': 1}
                    else:
                        stats[champ]['min'] = min(stats[champ]['min'], valeur)
                        stats[champ]['max'] = max(stats[champ]['max'], valeur)
                        stats[champ]['somme'] += valeur
                        stats[champ]['count'] += 1
                # Gestion des booléens
                elif isinstance(valeur, bool):
                    if champ not in stats:
                        stats[champ] = {'vrai': 0, 'faux': 0}
                    if valeur:
                        stats[champ]['vrai'] += 1
                    else:
                        stats[champ]['faux'] += 1
                # Gestion des listes (en considérant la taille de la liste)
                elif isinstance(valeur, list):
                    taille = len(valeur)
                    if champ not in stats:
                        stats[champ] = {'min_taille': taille, 'max_taille': taille, 'somme_taille': taille, 'count': 1}
                    else:
                        stats[champ]['min_taille'] = min(stats[champ]['min_taille'], taille)
                        stats[champ]['max_taille'] = max(stats[champ]['max_taille'], taille)
                        stats[champ]['somme_taille'] += taille
                        stats[champ]['count'] += 1

        # Finalisation des calculs
        for champ, stat in stats.items():
            if 'somme' in stat:  # Pour les champs numériques
                stat['moyenne'] = stat['somme'] / stat['count']
                del stat['somme'], stat['count']
            elif 'vrai' in stat:  # Pour les champs booléens, calcul du pourcentage
                total = stat['vrai'] + stat['faux']
                stat['% vrai'] = (stat['vrai'] / total) * 100 if total > 0 else 0
                stat['% faux'] = (stat['faux'] / total) * 100 if total > 0 else 0
                del stat['vrai'], stat['faux']
            elif 'somme_taille' in stat:  # Pour les champs liste, calcul de la moyenne de taille
                stat['moyenne_taille'] = stat['somme_taille'] / stat['count']
                del stat['somme_taille'], stat['count']
        return stats


    def parse_value(self, value):
        if isinstance(value, list):  # Si la valeur est déjà une liste, la retourner directement
            return value
        try:
            # Tente de convertir en float si c'est une représentation de nombre
            return float(value)
        except ValueError:
            # Si la conversion échoue, vérifie si la valeur est un booléen ou une liste séparée par des points-virgules
            if value.lower() in ['true', 'false']:
                return value.lower() == 'true'
            elif ';' in value:
                # Convertit les chaînes séparées par des points-virgules en listes
                return value.split(';')
            else:
                # Retourne la chaîne telle quelle si aucun des cas ci-dessus ne s'applique
                return value


    def display_stats(self, stats):
        stats_str = "\n".join([f"{champ}: {attributs}" for champ, attributs in stats.items()])
        messagebox.showinfo("Statistiques", stats_str)

    def update_combobox(self, champs_et_types):
        valeurs_combobox = [f"{champ} ({type_champ})" for champ, type_champ in champs_et_types]
        self.champs_combobox['values'] = valeurs_combobox
        if valeurs_combobox:
            self.champs_combobox.current(0)

    def update_treeview(self, champs, donnees):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = champs
        self.tree["show"] = "headings"
        for champ in champs:
            self.tree.heading(champ, text=champ)
            self.tree.column(champ, width=100)

        for item in donnees:
            valeurs = [item.get(champ, "") for champ in champs]
            self.tree.insert("", 'end', values=valeurs)
