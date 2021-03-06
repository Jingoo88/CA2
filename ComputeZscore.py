
import log
import threading
from numpy import exp


__author__ = "Thomas"

logger = log.setup_custom_logger('ComputeZscore')


class ComputeZscore(threading.Thread):

    def __init__(self, estimate, row, index, coeff=1):
        threading.Thread.__init__(self, target=self.score)
        self.estimate = estimate
        self.row = row
        self.coeff = coeff
        self.score = {"SCORE": 0}
        self.index = index
        self._return = None

    def run(self):

        if self._Thread__target is not None:
            self._return = self._Thread__target()

    def score(self):

        self.score["PRIX_PERSONNE"] = self.estimate.get_zscore(self.row["PRIX_PERSONNE"], "PRIX_PERSONNE",
                                                     (str(self.row["REGION"]), str(self.row["TYPE_BATEAU_AGREGE"])))
        self.score["SCORE"] += self.coeff["PRIX_PERSONNE"]*self.score["PRIX_PERSONNE"]

        self.score["PRIX_METRE"] = self.estimate.get_zscore(self.row["PRIX_METRE"], "PRIX_METRE",
                                                     (str(self.row["REGION"]), str(self.row["TYPE_BATEAU_AGREGE"])))
        self.score["SCORE"] += self.coeff["PRIX_METRE"]*self.score["PRIX_METRE"]

        to_exp = self.estimate.get_zscore(self.row["PRIX_PUISSANCE"],"PRIX_PUISSANCE",
                                          (str(self.row["REGION"]),str(self.row["TYPE_BATEAU_AGREGE"])))

        if to_exp > 4.6:

            self.score["PRIX_PUISSANCE"] = 100
        else:
            self.score["PRIX_PUISSANCE"] = exp(to_exp) - 1

        self.score["SCORE"] += self.coeff["PRIX_PUISSANCE"]*self.score["PRIX_PUISSANCE"]

        self.score["DELAIS_MOYEN_REPONSE_MESSAGES"] = self.estimate.get_zscore(self.row["DELAIS_MOYEN_REPONSE_MESSAGES"],
                                                     "DELAIS_MOYEN_REPONSE_MESSAGES",
                                                     (str(self.row["REGION"]), str(self.row["TYPE_BATEAU_AGREGE"])))
        self.score["SCORE"] += self.coeff["DELAIS_MOYEN_REPONSE_MESSAGES"]*self.score["DELAIS_MOYEN_REPONSE_MESSAGES"]

        self.score["TAUX_DE_TRANSFORMATION"] = self.estimate.get_zscore(self.row["TAUX_DE_TRANSFORMATION"],
                                                                        "TAUX_DE_TRANSFORMATION",
                                                                        (str(self.row["REGION"]),
                                                                         str(self.row["TYPE_BATEAU_AGREGE"])))
        self.score["SCORE"] += self.coeff["TAUX_DE_TRANSFORMATION"]*self.score["TAUX_DE_TRANSFORMATION"]

        if 0 < self.row["MOYENNE_EVALUATIONS_GLOBALE"] <= 4:
            self.score["MOYENNE_EVALUATIONS_GLOBALE"] = 2
            self.score["SCORE"] += self.coeff["MOYENNE_EVALUATIONS_GLOBALE"]*2

        if self.row["CO_NAV_UNIQUEMENT"] == 1:
            self.score["CO_NAV_UNIQUEMENT"] = 4
            self.score["SCORE"] += self.coeff["CO_NAV_UNIQUEMENT"]*4

        if self.row["A_QUAI_UNIQUEMENT"] == 1:
            self.score["A_QUAI_UNIQUEMENT"] = 1000
            self.score["SCORE"] += self.coeff["A_QUAI_UNIQUEMENT"]*1000

        if self.row["NB_IMAGES"] < 2:
            self.score["NB_IMAGES"] = 2
            self.score["SCORE"] += self.coeff["NB_IMAGES"]*2

        if self.row["ANNEE_CONSTRUCTION_AGREGE"] == "- de 10 ans":
            self.score["ANNEE_CONSTRUCTION_AGREGE"] = 1
            self.score["SCORE"] += self.coeff["ANNEE_CONSTRUCTION_AGREGE"]*1
        elif self.row["ANNEE_CONSTRUCTION_AGREGE"] == "- de 15 ans":
            self.score["ANNEE_CONSTRUCTION_AGREGE"] = 2
            self.score["SCORE"] += self.coeff["ANNEE_CONSTRUCTION_AGREGE"]*2
        elif self.row["ANNEE_CONSTRUCTION_AGREGE"] == "+ de 15 ans":
            self.score["ANNEE_CONSTRUCTION_AGREGE"] = 3
            self.score["SCORE"] += self.coeff["ANNEE_CONSTRUCTION_AGREGE"]*3
        else:
            self.score["ANNEE_CONSTRUCTION_AGREGE"] = 0
            self.score["SCORE"] += self.coeff["ANNEE_CONSTRUCTION_AGREGE"]*0

        return self.score, self.index

    def join(self):
        threading.Thread.join(self)
        return self._return
