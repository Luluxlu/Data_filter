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
        self.entetes = None
        self.data_display = None
        self.save_button = None
        self.load_button = None
        self.champs_combobox = None
        self.tree = None
        self.scrollbar = None
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

        # Création du tableau (Treeview)
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill='both', pady=10)

        # Association de l'événement de clic avec la méthode on_click
        self.tree.bind('<Button-1>', self.on_click)

        # Scrollbar pour le Treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Combobox pour les champs détectés
        self.champs_combobox = ttk.Combobox(self, state="readonly", width=60)
        self.champs_combobox.pack(pady=5)

    def on_click(self, event):
        # Identifier l'item sur lequel le clic a eu lieu
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # S'assurer que le clic est sur une cellule valide
        if item_id and column:
            # Calculer la position de la cellule
            x, y, width, height = self.tree.bbox(item_id, column)

            # Créer un widget Entry pour éditer la valeur
            entry = tk.Entry(self.tree, width=width)
            entry.place(x=x, y=y, width=width, height=height)

            # Pré-remplir l'Entry avec la valeur actuelle
            value = self.tree.item(item_id, 'values')[int(column[1:]) - 1]  # Modifier pour obtenir la valeur correcte
            entry.insert(0, value)

            # Focus sur l'Entry et sélectionner le texte
            entry.focus_force()
            entry.select_range(0, tk.END)

            # Fonction pour sauvegarder la nouvelle valeur lorsque l'Entry perd le focus
            def save_edit(event):
                self.tree.set(item_id, column, entry.get())
                entry.destroy()

            # Lier la perte de focus à la sauvegarde de la modification
            entry.bind("<FocusOut>", save_edit)
            entry.bind("<Return>", save_edit)

    def update_combobox(self, champs_et_types):
        # Formater les entrées pour inclure le type à côté du nom du champ
        valeurs_combobox = [f"{champ} ({type_champ})" for champ, type_champ in champs_et_types]
        self.champs_combobox['values'] = valeurs_combobox
        if valeurs_combobox:
            self.champs_combobox.current(0)

    def update_treeview(self, champs, donnees):
        # Nettoyer le tableau existant
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Définir les nouvelles colonnes
        self.tree["columns"] = champs
        self.tree["show"] = "headings"

        # Configurer les entêtes et la largeur des colonnes
        for champ in champs:
            self.tree.heading(champ, text=champ)
            self.tree.column(champ, width=100)

        # Insérer les nouvelles données
        for item in donnees:
            valeurs = [item.get(champ, "") for champ in champs]
            self.tree.insert("", 'end', values=valeurs)

    def extraire_donnees_treeview(self):
        donnees = []
        for ligne in self.tree.get_children():
            valeurs_ligne = self.tree.item(ligne)['values']
            donnees.append(valeurs_ligne)
        return donnees

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

            # Mise à jour de la liste déroulante et de l'affichage
            self.update_combobox(champs)

            champs = [champ for champ, _ in champs]  # Extraire juste les noms des champs
            self.update_treeview(champs, donnees_formattees)

    def save_data(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            extension = file_path.split('.')[-1].lower()
            donnees = self.extraire_donnees_treeview()
            if extension == 'csv':
                sauvegarder_en_csv(self, donnees, file_path, self.entetes)
            elif extension == 'json':
                sauvegarder_en_json(self, donnees, file_path)
            elif extension == 'xml':
                sauvegarder_en_xml(self, donnees, file_path)
            elif extension in ['yaml', 'yml']:
                sauvegarder_en_yaml(self, donnees, file_path)
            else:
                messagebox.showerror("Erreur", "Type de fichier non supporté.")
