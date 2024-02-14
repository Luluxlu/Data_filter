from view.interface import Application
import tkinter as tk

from tkinter import messagebox

class StatsApp(Application):
    def __init__(self):
        super().__init__()
        self.stats = {}
        self.data = []
        self.create_widgets_specific_to_stats_app()
        print("StatsApp initialisée.")

    def load_data_and_calculate_stats(self):
        # Exemple de pseudo-code pour charger les données sans les effacer
        if not self.data:  # Supposons que vous ne voulez charger les données que si elles ne sont pas déjà chargées
            # Chargement des données ici dans self.data
            pass  # Remplacez ceci par votre logique de chargement des données réelle

        
        # Ici, vous chargeriez vos données dans self.data
        # Pour l'exemple, supposons que self.data soit déjà rempli avec les données chargées
        self.calculate_stats()
        self.update_treeview_with_stats()

    def parse_value(value):
        """Convertit une valeur chaîne en son type approprié (float, bool, list, ou str)."""
        if value.replace('.', '', 1).isdigit():
            return float(value)
        elif value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        elif ';' in value:
            return value.split(';')
        else:
            return value  # Garde la chaîne telle quelle si aucun autre cas ne correspond

    def calculate_stats(self, donnees_formattees):
        stats = {}
        # Conversion des données au format approprié
        for donnee in donnees_formattees:
            for champ, valeur_str in donnee.items():
                valeur = parse_value(valeur_str)  # Convertit la valeur en son type approprié
                if isinstance(valeur, float):  # Exemple pour les valeurs numériques
                    if champ not in stats:
                        stats[champ] = {'min': valeur, 'max': valeur, 'somme': valeur, 'count': 1}
                    else:
                        stats[champ]['min'] = min(stats[champ]['min'], valeur)
                        stats[champ]['max'] = max(stats[champ]['max'], valeur)
                        stats[champ]['somme'] += valeur
                        stats[champ]['count'] += 1
        # Calcul de la moyenne pour les champs numériques
        for champ, stat in stats.items():
            if 'somme' in stat:  # Vérifie si le champ est numérique
                stat['moyenne'] = stat['somme'] / stat['count']
                del stat['somme'], stat['count']  # Supprime 'somme' et 'count' qui ne sont plus nécessaires
        
        return stats

    def extraire_valeur(self, item, champ):
        # Cette méthode extrait la valeur pour le champ donné en tenant compte du type
        return item.get(champ, 0 if champ in item and isinstance(item[champ], (int, float)) else False if champ in item and isinstance(item[champ], bool) else [])
         

    def calculer_stats_numeriques(self, valeurs):
        if not valeurs: return {"min": 0, "max": 0, "moyenne": 0}
        min_val = min(valeurs)
        max_val = max(valeurs)
        moyenne = sum(valeurs) / len(valeurs)
        return {"min": min_val, "max": max_val, "moyenne": moyenne}

    def calculer_stats_booleens(self, valeurs):
        nb_vrai = valeurs.count(True)
        total = len(valeurs)
        if total == 0: return {"% vrai": 0, "% faux": 0}
        return {"% vrai": (nb_vrai / total) * 100, "% faux": ((total - nb_vrai) / total) * 100}

    def calculer_stats_listes(self, valeurs):
        tailles = [len(v) for v in valeurs]
        return self.calculer_stats_numeriques(tailles)

    def update_treeview_with_stats(self):
        # Cette méthode suppose l'existence d'un moyen d'effacer et de mettre à jour le Treeview avec les nouvelles statistiques
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        for champ, stats_champ in self.stats.items():
            champ_id = self.tree.insert("", 'end', text=champ, values=(champ,))
            for stat_nom, stat_valeur in stats_champ.items():
                self.tree.insert(champ_id, 'end', text=f"{champ} {stat_nom}", values=[f"{stat_nom}: {stat_valeur}"])
    
    def afficher_stats(self):
        # Création d'une nouvelle fenêtre pour les statistiques
        fenetre_stats = tk.Toplevel(self)
        fenetre_stats.title("Statistiques des Données")

        # Utilisation d'un widget Text pour afficher les statistiques
        texte_stats = tk.Text(fenetre_stats, wrap="word")
        texte_stats.pack(expand=True, fill="both", padx=10, pady=10)

        # Vérifiez si self.stats contient des données
        if not self.stats:
            texte_stats.insert("end", "Aucune statistique à afficher.\n")
        else:
            # Génération du texte des statistiques
            for champ, stats_champ in self.stats.items():
                texte_stats.insert("end", f"Champ: {champ}\n")
                for stat_nom, stat_valeur in stats_champ.items():
                    # Assurez-vous que stat_valeur est un string pour éviter des erreurs
                    texte_stats.insert("end", f"  {stat_nom}: {str(stat_valeur)}\n")
                texte_stats.insert("end", "\n")

        # Désactivation de l'édition du widget Text
        texte_stats.config(state="disabled")

    def create_widgets_specific_to_stats_app(self):

        # Ajoutez ici le bouton spécifique à StatsApp pour afficher les statistiques
        load_button = tk.Button(self, text="Charger et Calculer Statistiques", command=self.load_data_and_calculate_stats)
        load_button.pack()
        print("Widgets spécifiques à StatsApp créés.")