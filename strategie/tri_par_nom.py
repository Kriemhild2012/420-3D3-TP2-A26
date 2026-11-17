from strategie_tri import StrategieTri
class TriParNom(StrategieTri):

    def trier(self, produits: list) -> list:
        return sorted(produits, key=lambda p: p.nom.lower())