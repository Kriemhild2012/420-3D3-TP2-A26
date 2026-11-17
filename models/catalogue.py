import json
from composite import Bundle
from feuille import ProduitNumerique
from composant import Composant
from strategie.strategie_tri import StrategieTri
from strategie.tri_par_nom import TriParNom
from strategie.tri_par_prix import TriParPrix
from strategie.tri_par_popularite import TriParPopularite

class Catalogue:

    def __init__(self, chemin_json: str, strategie_tri: StrategieTri = None):
        self._produits: dict[int, Composant] = {}
        self._charger(chemin_json)
        self._strategie_tri = strategie_tri or TriParNom()  # Stratégie par défaut

    def _charger(self, chemin: str) -> None:
        with open(chemin, encoding="utf-8") as f:
            donnees = json.load(f)

        for d in donnees:
            if d["type"] == "produit":
                produit = ProduitNumerique(
                    id=d["id"],
                    nom=d["nom"],
                    description=d["description"],
                    prix=d["prix"],
                    nb_ventes=d["nb_ventes"],
                    image_url=d["image_url"]
                )
            else:
                produit = Bundle(
                    id=d["id"],
                    nom=d["nom"],
                    description=d["description"],
                    #prix=d["prix"],
                    nb_ventes=d["nb_ventes"],
                    image_url=d["image_url"],
                    rabais=d.get("rabais", 0.0)
                )
            self._produits[produit.id] = produit

        for d in donnees:
            if d["type"] == "bundle":
                bundle = self._produits[d["id"]]
                for enfant_id in d.get("enfants", []):
                    bundle.ajouter_items(self._produits[enfant_id])

    def tous(self) -> list:
        return list(self._produits.values())

    def obtenir(self, id: int):
        return self._produits.get(id)

    def definir_strategie_tri(self, strategie):
        self._strategie_tri = strategie

    def afficher_produits(self) -> list:
        resultat = self._strategie_tri.trier(self.tous())
        produits = self.tous()

        # Application du patron Stratégie
        produits = self._strategie_tri.trier(produits)

        resultat = []

        for p in produits:

            if affichage == "compact":

                resultat.append({
                    "id": p.id,
                    "nom": p.nom,
                    "prix_total": p.prix_total(),
                    "image_url": p.image_url,
                    "est_bundle": p.est_bundle(),
                })

            elif affichage == "detaille":

                donnees = {
                    "id": p.id,
                    "nom": p.nom,
                    "prix_total": p.prix_total(),
                    "image_url": p.image_url,
                    "description": p.description,
                    "nb_ventes": p.nb_ventes,
                    "est_bundle": p.est_bundle(),
                }

                if p.est_bundle():
                    donnees["nb_items"] = p.nb_items()

                resultat.append(donnees)

        return resultat

  
catalogue = Catalogue("catalogue.json", TriParPrix())

# Trier par prix
produits = catalogue.afficher_produits("compact")

# Changer de stratégie : popularité
catalogue.definir_strategie_tri(TriParPopularite())

# Trier par popularité
produits = catalogue.afficher_produits("detaille")

# Changer de stratégie : nom
catalogue.definir_strategie_tri(TriParNom())

# Trier par nom
produits = catalogue.afficher_produits("compact")