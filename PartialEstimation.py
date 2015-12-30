
import log
from pickle import load
from math import isnan


__author__ = 'Thomas'

logger = log.setup_custom_logger('Estimation')


class PartialEstimation:
    """
    Class computing vars and means for variables used for score estimates and then calculating zcores
    Basicly the calculating tool of the library
    """

    def __init__(self):

        logger.info("Initializing PartialEstimation object")

        self.__means = self.load_obj("last_estimated_means")
        self.__std = self.load_obj("last_estimated_vars")

        logger.info("Estimation object initialized")

    @staticmethod
    def load_obj(name):

        with open(name + '.pkl', 'rb') as f:
            return load(f)

    def get_zscore(self, value, var, carac):
        """
        Method to compute zscore for given parameters
        :param value: value of the variable realization as a real
        :param var: name of the variable as a string
        :param carac: list of REGION and TYPE (in this order) associated with the realization
        :return: computed zscore
        """

        try:

            self.zscore = (value - self.__means[var][carac]) / self.__std[var][carac]

        except KeyError:
            self.zscore = 2
        except RuntimeWarning:
            self.zscore = 2
            print "tit"

        if self.zscore > 1000:

            self.zscore = 1000

        elif self.zscore < -1000:

            self.zscore = -1000

        elif isnan(self.zscore):

            self.zscore = 100

        return self.zscore


if __name__ == '__main__':

    print "Main motherfucker"
