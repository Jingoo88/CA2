

import pandas as pd
import os
import datetime
import log

from numpy.random import uniform
from sys import exit

__author__ = 'Thomas'

logger = log.setup_custom_logger('Data')


class Data:
    """
    Data processing class, built in methods clean data, fill NAs ... for estimation purposes
    """

    def __init__(self, data_handler):

        logger.info("Initializing Data object")

        self.__now = datetime.datetime.now()
        self.__headers = []
        self.__data = {}
        self.__data_handler = data_handler

        logger.info("Data object initialized")

    def __get_csv(self, path):
        """
        recuperation du csv
        a modifier selon la methode choisie pour recuperer les donnees
        :param path: Path of the CSV
        :return: None
        """

        assert (os.path.exists(path)), ["CSV FILE COULD NOT BE FOUND AT " + path, logger.critical('NO CSV FILE FOUND')]

        self.row_table = pd.DataFrame.from_csv(path, sep=";")

        logger.info('file found')
        assert (type(self.row_table) == pd.core.frame.DataFrame), ["CSV CONVERSION TO DATA FRAME FAILED",
                                                                   logger.info('CSV CONVERSION TO DATA FRAME FAILED')]
        self.__headers = list(self.row_table.columns.values)

        logger.info('conversion to pandas dataframe successfull')

    def __get_table(self, query, **kwargs):
        """
        Method to get table in base via DataHandler instance
        :param query: SQL query as string
        :return: None
        """

        if bool(kwargs):
            self.row_table = self.__data_handler.extract_from_table(query, type=kwargs)
        else:
            self.row_table = self.__data_handler.extract_from_table(query)

    def __construction_year_to_categories(self):
        """
        Method binning construction year to categories
        :param: None
        :return: None
        """

        assert ("ANNEE_CONSTRUCTION" in self.row_table), ["TABLE HAS NO 'ANNEE_CONSTRUCTION' ROW",
                                                          logger.error("TABLE HAS NO 'ANNEE_CONSTRUCTION' ROW")]

        logger.info("Discretizing 'annee construction'")

        annee_temp = pd.cut(self.row_table["ANNEE_CONSTRUCTION"], bins=[-1, self.__now.year-15, self.__now.year-10,
                                                                        self.__now.year-5, self.__now.year + 1000],
                            labels=["+ de 15 ans", "- de 15 ans", "- de 10 ans", "- de 5 ans"])

        self.row_table["ANNEE_CONSTRUCTION_AGREGE"] = pd.Series(data=annee_temp)
        logger.info("'Annee_construction' successfully discretized")

    def __boat_type_to_categories(self):
        """
         Method binning boat type to categories
         :param: None
        :return: None
        """

        assert ("TYPE_BATEAU_ID" in self.row_table), ["TABLE HAS NO 'TYPE_BATEAU_ID' ROW",
                                                      logger.error("TABLE HAS NO 'TYPE_BATEAU_ID' ROW")]

        logger.info("Discretizing 'type_bateau_id'")

        type_temp = pd.cut(self.row_table["TYPE_BATEAU_ID"], bins=[-1, 0, 1, 2, 3, 4, 6],
                           labels=["Autre", "Voilier", "Moteur", "Voilier1", "Moteur1", "Autre1"])

        type_temp = pd.Series(data=type_temp)
        type_temp.replace({"Moteur1": "Moteur", "Voilier1": "Voilier", "Autre1": "Autre"}, inplace=True)

        self.row_table["TYPE_BATEAU_AGREGE"] = type_temp
        logger.info("'Type_bateau_id' successfully discretized")

    def __get_month(self):
        """
         Get ticket month via the pandas datetime
         :param: None
        :return: None
        """

        logger.info("Getting date to month conversion")

        try:
            self.row_table["MOIS_RESA"] = pd.to_datetime(self.row_table["DATE_CREA_RESERVATION"], dayfirst=True).dt.month
            self.row_table["MOIS_RESA"] = self.row_table["MOIS_RESA"].astype(str)
            logger.info("Date to month conversion successful")

        except KeyError as e:
            logger.info("No %s key, passing"%e)

    def __fill_na(self):
        """
         Method to fill NAs (NULL values in SQL database).
         2015/12/02 : Hard designed for any possible issue this should be changed
         :param: None
        :return: None
        """

        logger.info("replacing NAs")

        try:
            self.row_table["NOTE_MOYENNE_DATE_TICKET"].fillna(0, inplace=True)
            logger.warning("Some NAs filled in Note moyenne -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column Note moyenne -- passing")
            pass

        try:
            self.row_table["DELAIS_MOYEN_REPONSE_MESSAGES"].fillna(uniform(low=24, high=50), inplace=True)
            logger.warning("Some NAs filled in delais_reponse_message -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column delais_reponse_message -- passing")
            pass

        try:
            self.row_table["CAPACITE_CONSEILLEE"].fillna(1, inplace=True)
            logger.warning("Some NAs filled in capacite_conseillee -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column capacite_conseillee -- passing")
            pass

        try:
            self.row_table["LONGUEUR"].fillna(1, inplace=True)
            logger.warning("Some NAs filled in longueur -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column capacite_conseillee -- passing")
            pass

        try:
            self.row_table["ANNEE_CONSTRUCTION"].fillna(1990, inplace=True)
            logger.warning("Some NAs filled in Annee_construction -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column Annee_construction -- passing")
            pass

        try:
            self.row_table["PUISSANCE_MOTEUR"].fillna(1, inplace=True)
            logger.warning("Some NAs filled in Puissance -- please try to avoid NAs")
        except KeyError:
            logger.info("Table has no column Puissance -- passing")
            pass
        logger.info("NAs replaced")

    def __replace_zero(self):
        """
         Method replace zeros (cold cause problems with following estimates).
         2015/12/02 : Hard designed for any possible issue this should be changed
         :param: None
        :return: None
        """

        logger.info("Replacing zeros")
        self.row_table.loc[self.row_table["LONGUEUR"] == 0, "LONGUEUR"] = 1
        logger.info("Zeros replaced in Longueur")
        self.row_table.loc[self.row_table["PUISSANCE_MOTEUR"] == 0, "PUISSANCE_MOTEUR"] = 1
        logger.info("Zeros replaced in Puissance")

        try:
            self.row_table.loc[self.row_table["PRIX_JOURNEE_DATE_TICKET"] == 0, "PRIX_JOURNEE_DATE_TICKET"] = 100 #a modifier!!!!!!!!!!!!!

        except KeyError:
            pass

        try:
            self.row_table.loc[self.row_table["DELAIS_MOYEN_REPONSE_MESSAGES"] == 0,
                               "DELAIS_MOYEN_REPONSE_MESSAGES"] = 24
            logger.info("Zeros replaced in delais_moyen_reponse")
        except KeyError:
            logger.info("Table has no column delais_moyen_reponse -- passing")
            pass

        logger.info("Zeros replaced")

    def __get_ratios(self):
        """
         Method to compute ratios as new variables
         2015/12/02 : Hard designed for any possible issue this should be changed
         :param: None
        :return: None
        """

        logger.info("Computing ratios")

        try:

            self.row_table["PRIX_PERSONNE"] = self.row_table["PRIX_JOURNEE_DATE_TICKET"] /\
                                              self.row_table["CAPACITE_CONSEILLEE"]
            self.row_table["PRIX_METRE"] = self.row_table["PRIX_JOURNEE_DATE_TICKET"] /\
                                           self.row_table["LONGUEUR"]
            self.row_table["PRIX_PUISSANCE"] = self.row_table["PRIX_JOURNEE_DATE_TICKET"] /\
                                               self.row_table["PUISSANCE_MOTEUR"]
            self.row_table["TAUX_DE_TRANSFORMATION"] = self.row_table["NB_RESERVATIONS_DATE_TICKET"] / \
                                                       (self.row_table["NB_INTERLOCUTEURS_DATE_TICKET"] + 1)
            self.row_table["PUISSANCE_PERSONNE"] = self.row_table["PUISSANCE_MOTEUR"] /\
                                                   self.row_table["CAPACITE_CONSEILLEE"]

            logger.info("Ratios prix/personne, prix/metre, prix/puissance, taux_transformation,"
                        " puissance/personne successfully computed ")

        except KeyError as e:

            logger.info("Table has no key named %s, trying second set of keys" %e)

            try:

                self.row_table["PRIX_PERSONNE"] = self.row_table["PRIX_HAUTE_SAISON_JOURNEE"] /\
                                                  self.row_table["CAPACITE_CONSEILLEE"]
                self.row_table["PRIX_METRE"] = self.row_table["PRIX_HAUTE_SAISON_JOURNEE"] /\
                                               self.row_table["LONGUEUR"]
                self.row_table["PRIX_PUISSANCE"] = self.row_table["PRIX_HAUTE_SAISON_JOURNEE"] /\
                                                   self.row_table["PUISSANCE_MOTEUR"]
                self.row_table["PUISSANCE_PERSONNE"] = self.row_table["PUISSANCE_MOTEUR"] /\
                                                       self.row_table["CAPACITE_CONSEILLEE"]
                self.row_table["TAUX_DE_TRANSFORMATION"] = self.row_table["NB_ACCEPTEE"] /\
                                                           (self.row_table["NB_INTERLOCUTEURS"] + 1)

                logger.info("Ratios prix/personne, prix/metre, prix/puissance, taux_transformation,"
                            " puissance/personne successfully computed ")

            except KeyError as e:

                logger.critical("Table has no key named %s, can't compute ratios programme will now exit" %e)
                exit("CRITICAL ERROR, no key named %s" %e)

    def get_clean_data(self, query, **kwargs):
        """
         Get clean data via CSV
         :param path: CSV path
        :return: Row table cleaned
        """

        logger.info("Getting clean data")

        self.__get_table(query, type=kwargs)

        logger.info("Clean data generated -- processing")

    def get_clean_datab(self, query):

        """
         Get clean data via SQL
         :param query: SQL query as string
        :return: Row table cleaned
        """

        logger.info("Getting clean data")

        self.__get_table(query)
        self.__replace_zero()
        self.__get_month()
        self.__fill_na()
        self.__boat_type_to_categories()
        self.__construction_year_to_categories()
        self.__get_ratios()

        logger.info("Clean data generated -- processing")

        return self.row_table


if __name__ == '__main__':

    print "Main motherfucker"