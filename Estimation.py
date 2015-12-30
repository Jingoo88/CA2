
import log
import pickle

from math import isnan
from Data import Data

__author__ = 'Thomas'

logger = log.setup_custom_logger('Estimation')


class Estimation:
    """
    Class computing vars and means for variables used for score estimates and then calculating zcores
    Basicly the calculating tool of the library
    """

    def __init__(self, query, data_handler):

        logger.info("Initializing Estimation object")
        self.__data = Data(data_handler)
        self.__data = self.__data.get_clean_datab(query)

        self.__bygroup = self.__data.groupby(["REGION", "TYPE_BATEAU_AGREGE"])

        self.__means = {}
        self.__std = {}

        logger.info("Estimation object initialized")

    def get_means(self, variables):
        """
        Method computing once and for all the different means later used in the zscore computations
        :param variables: list of variables name to compute means on, as list of strings
        :return: None
        """

        logger.info("Starting means computing")

        for var in variables:

            self.__means[var] = self.__bygroup[var].mean()

            logger.info("%s means computed"%var)

        self.save_obj(self.__means, "last_estimated_means")

    def get_deviations(self, variables):
        """
        Method computing once and for all the different var later used in the zscore computations
        :param variables: list of variables name to compute var on, as list of strings
        :return: None
        """

        logger.info("Starting deviations computing")

        for var in variables:

            self.__std[var] = self.__bygroup[var].std()

            logger.info("%s deviations computed"%var)

        self.save_obj(self.__std, "last_estimated_vars")

    @staticmethod
    def save_obj(obj, name):

        with open(name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_obj(name):

        with open(name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def get_zscore(self, value, var, carac):
        """
        Method to compute zscore for given parameters
        :param value: value of the variable realization as a real
        :param var: name of the variable as a string
        :param carac: list of REGION and TYPE (in this order) associated with the realization
        :return: computed zscore
        """

        try:

            if self.__std[var][carac] > 0.001:

                self.zscore = (value - self.__means[var][carac]) / self.__std[var][carac]
            else:
                self.zscore = (value - self.__means[var][carac]) / 0.001

        except KeyError:
            self.zscore = 2

        if self.zscore > 1000:

            self.zscore = 1000

        elif self.zscore < -1000:

            self.zscore = -1000

        elif isnan(self.zscore):

            self.zscore = 100

        return self.zscore


if __name__ == '__main__':

    print "Main motherfucker"
