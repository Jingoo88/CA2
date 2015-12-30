__author__ = 'Administrateur'


import time
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from Data import Data
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import csv



t = time.time()

data = Data()
data = data.get_clean_data('C:/Users/Administrateur/Documents/Click&Boat/Thomas/EXTRACT_ANALYSE_2.csv')
"""
data_quali = data.drop(["ID_BATEAU", "NB_PHOTOS_DATE_TICKET", "NB_DEMANDES_TOTAL_DATE_TICKET", "LONGUEUR",
                        "ANNEE_CONSTRUCTION", "CAPACITE_AUTORISEE", "DATE_CREA_RESERVATION", "LOCALISATION_ADRESSE",
                        "PRIX_JOURNEE_DATE_TICKET", "NB_RESERVATIONS_DATE_TICKET", "NB_INTERLOCUTEURS_DATE_TICKET",
                        "PUISSANCE_MOTEUR", "NB_JOURS", "PRIX_PERSONNE", "PRIX_METRE", "PRIX_PONDERE", "PRIX_PUISSANCE",
                        "NOTE_MOYENNE_DATE_TICKET", "NB_DEMANDES_ACCEPTE_DATE_TICKET", "NB_DEMANDES_REFUSE_DATE_TICKET",
                        "NB_DEMANDES_EXPIRE_DATE_TICKET", "NOTE_MOYENNE_DATE_TICKET", "TYPE_BATEAU_ID"],axis=1)


data_indic = pd.DataFrame(pd.get_dummies(data_quali[["REGION", "TYPE_BATEAU_AGREGE", "ANNEE_CONSTRUCTION_AGREGE", "MOIS_RESA"]]))
"""

data_quanti = [c for c, d in zip(data.columns, data.dtypes) if ((d == np.int64 or d == np.float64)
                                                                and c not in ["MOIS_RESA"])]
data_quali = [c for c in data.columns if c not in data_quanti and
              c not in ["DATE_CREA_RESERVATION", "LOCALISATION_ADRESSE"] or c == "ID_TICKET"]


num = data[data_quanti]
cat = data[data_quali]

cat_exp_df = pd.DataFrame(pd.get_dummies(cat))


#reject = ['ANNEE_CONSTRUCTION_AGREGE_+ de 15 ans', 'MOIS_RESA_6', 'REGION_ Aquitaine ', 'TYPE_BATEAU_AGREGE_Autre']
reject = []
keep = [c for c in cat_exp_df.columns if c not in reject]

cat_exp_df_nocor = cat_exp_df[keep]


X = pd.concat([num, cat_exp_df], axis=1)


reject = ["ID_BATEAU", "ANNEE_CONSTRUCTION", "TYPE_BATEAU_ID"]
keep = [c for c in X.columns if c not in reject]

np.random.seed(5)


estimator = KMeans(n_clusters=5)
res = estimator.fit(X)


f = open("C:/Users/Administrateur/Documents/Click&Boat/test.txt", "w")
f.write(res.labels_)

"""
nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)
print indices
print distances

or i in list(X.columns.values):
    print i
    print np.any(np.isnan(X[i]))

print np.any(np.isnan(X))
"""






















