from view.interface import Application
import tkinter as tk

from tkinter import messagebox

class StatsApp(Application):
    def __init__(self):
        super().__init__()
        self.stats = {}
        self.create_widgets_specific_to_stats_app()

    def load_data(self):
        super().load_data()
        self.calculate_stats()
        self.update_treeview_with_stats()

    def calculate_stats(self):
        print("La méthode calculate_stats() est appelée.")
        self.stats = {}

        for item in self.donnees_avec_types:

            if not isinstance(item, tuple) or len(item) != 2:
                print(f"Erreur: Le tuple {item} ne contient pas exactement deux éléments.")
                continue
             
            champ, type_champ = item
            valeurs = [self.extraire_valeur(item, champ) for item in self.donnees_formattees]
            if type_champ in [int, float]:
                self.stats[champ] = self.calculer_stats_numeriques(valeurs)
            elif type_champ == bool:
                self.stats[champ] = self.calculer_stats_booleens(valeurs)
            elif type_champ == list:
                self.stats[champ] = self.calculer_stats_listes(valeurs)

    def extraire_valeur(self, item, champ):
        # Cette méthode extrait la valeur pour le champ donné en tenant compte du type
        valeur = item.get(champ, 0 if isinstance(item[champ], (int, float)) else False if isinstance(item[champ], bool) else [])
        return valeur

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
        self.stats_button = tk.Button(self, text="Afficher Statistiques", command=self.afficher_stats)
        self.stats_button.pack(pady=5)