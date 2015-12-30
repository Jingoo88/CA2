
import log
from Data import Data
from PartialEstimation import PartialEstimation
from ComputeZscore import ComputeZscore

__author__ = 'Thomas'

logger = log.setup_custom_logger("Score")


class PartialScore:

    def __init__(self, coeff, query, data_handler, ids):

        logger.info("Initializing Score object")

        self.data = Data(data_handler)
        self.data = self.data.get_clean_datab(query)
        self.coeff = coeff
        self.requested_ids = ids
        self.score = {}
        self.score_details = {}
        self.continuous_variables = ["PUISSANCE_PERSONNE", "TAUX_DE_TRANSFORMATION", "PRIX_PERSONNE",
                                     "PRIX_METRE", "PRIX_PUISSANCE", "DELAIS_MOYEN_REPONSE_MESSAGES"]

        self.estimate = PartialEstimation()

        logger.info("Score object initialized")

    def __get_score(self):

        logger.info("Starting score computation")
        row_iterator = self.data.iterrows()

        count = 0  # iteration counter for lazy people

        for i, row in row_iterator:

            count += 1

            thread = ComputeZscore(self.estimate, row, i, self.coeff)
            thread.start()

            dic, ind = thread.join()
            self.score[ind] = dic


        logger.info("Computed %i scores"%count)

        return self.score

    def print_for_flo(self):

        self.__get_score()

        list_to_print = []

        for i in self.requested_ids:

            if int(i) in self.score:

                list_to_print.append(str(self.score[int(i)]["SCORE"]))

        print ', '.join(list_to_print)


if __name__ == '__main__':

    print "useless fool"
