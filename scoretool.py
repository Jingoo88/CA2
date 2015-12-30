
            if row["TYPE_BATEAU_AGREGE"] == "Moteur":  # a remplacer par une indicatrice propre

                temp10 = coeff * self.estimate.get_zscore(row["PUISSANCE_PERSONNE"], "PUISSANCE_PERSONNE",
                                                          (str(row["REGION"]), str(row["TYPE_BATEAU_AGREGE"])))
            else:
                temp10 = 0
            # coeff avant ou apres?

            """
            Seuils a refaire proprement
            """
            if 0 < row["MOYENNE_EVALUATIONS_GLOBALE"] < 4:
                temp5 = 2
            if row["CO_NAV_UNIQUEMENT"] == 1:
                temp6 = 4
            if row["A_QUAI_UNIQUEMENT"] == 1:
                temp13 = 1000
            if row["NB_IMAGES"] < 2:
                temp7 = 2
            if row["TYPE_BATEAU_AGREGE"] == "Autre":
                temp11 += 6
            if row["PHOTO_PROFIL"] == 0:
                temp8 = 0.5
            if row["ANNEE_CONSTRUCTION_AGREGE"] == "- de 5 ans":
                temp9 = 0
            elif row["ANNEE_CONSTRUCTION_AGREGE"] == "- de 10 ans":
                temp9 = 0.5
            elif row["ANNEE_CONSTRUCTION_AGREGE"] == "- de 15 ans":
                temp9 = 1.5
            else:
                temp9 = 2.5

            self.score[i] = temp1 + temp2 + temp3 + temp4 + temp5 + temp6 +\
                            temp13 + temp7 + temp8 + temp9 - temp10 + temp11 - temp12