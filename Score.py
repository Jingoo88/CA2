
import numpy as np
import log
from Data import Data
from Estimation import Estimation
from ComputeZscore import ComputeZscore

__author__ = 'Thomas'

logger = log.setup_custom_logger("Score")


class Score:

    def __init__(self, query1, query2, query3, data_handler):

        logger.info("Initializing Score object")

        self.data = Data(data_handler)
        self.data = self.data.get_clean_datab(query1)
        self.estimate = Estimation(query2, data_handler)
        self.query3 = query3
        self.coeff = {}
        self.score = {}
        self.score_details = {}
        self.coeff = {"PUISSANCE_PERSONNE":1, "TAUX_DE_TRANSFORMATION":1, "PRIX_PERSONNE":1,
                                     "PRIX_METRE":1, "PRIX_PUISSANCE":1, "DELAIS_MOYEN_REPONSE_MESSAGES":1}

        self.continuous_variables = ["PUISSANCE_PERSONNE", "TAUX_DE_TRANSFORMATION", "PRIX_PERSONNE",
                                     "PRIX_METRE", "PRIX_PUISSANCE", "DELAIS_MOYEN_REPONSE_MESSAGES"]

        self.estimate.get_deviations(self.continuous_variables)
        self.estimate.get_means(self.continuous_variables)

        logger.info("Score object initialized")

    def get_score(self):

        logger.info("Starting score computation")

        row_iterator = self.data.iterrows()

        count = 0  # iteration counter for lazy people
        doudou = []

        for i, row in row_iterator:

            count += 1
            if i in self.score.keys():
                print i

            thread = ComputeZscore(self.estimate, row, i, self.coeff)
            thread.start()

            dic, ind = thread.join()
            self.score[ind] = dic

        logger.info("Computed %i scores"%count)

        return self.score

    def get_coeff(self, data_handler):

        table = data_handler.extract_from_table(self.query3, kwargs="ts")

        iter = table.iterrows()

        for i, row in iter:

            self.coeff[row["NOM"]] = row["COEFF"]

    @staticmethod
    def dict_to_sorted_array(result):

        names = ['id', 'data']
        formats = ['int32', 'f8']
        dtype = dict(names=names, formats=formats)
        array = np.fromiter(result.iteritems(), dtype=dtype, count=len(result))
        array = np.sort(array, order="data")

        return array

    @staticmethod
    def get_script(result):

        count = 0
        f = open("C:/Users/Administrateur/Documents/Click&Boat/Thomas/test.bat", "w")
        f.write('@echo off\n"C:\Program Files\Google\Chrome\Application\chrome.exe\nsleep 2\n')
        for i, j in result:

            if count < 20:
                f.write('start chrome "https://www.clickandboat.com/en/back-office/3?id=' + str(i) + '"\n')
                count += 1
            else:
                break

        f.write(':FIN')
        f.close()


if __name__ == '__main__':

    print "useless fool"
