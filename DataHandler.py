
import pandas as pd
import log
from UpdateTable import UpdateTable
from sqlalchemy import create_engine, MetaData, Table


__author__ = 'Thomas'

logger = log.setup_custom_logger('DataHandler')


class DataHandler:
    """
    Class connecting to the database and handling all reading/writing operations via a sqlachemy engine
    Default dialect is MySQL, this can be changed via the constructor
    Connection information and target database are passed through the constructor
    The DataHandler constructor immediately creates a MetaData object to map the database
    2015/12/01 : Constructor is hard coded for a 'test' table, this should be changed in prod
    2015/12/01 : Extraction method is hard coded for this situation, this should be changed in prod
    """

    def __init__(self, usr, table, url, pwd=None, dialect="mysql+mysqldb"):

        logger.info("Initializing DataHandler object")
        self.usr = usr
        self.table = table
        self.url = url
        self.dialect = dialect
        self.pwd = pwd

        if self.pwd is None:

            self.engine_request = self.dialect + "://" + self.usr + "@" + self.url + "/" + self.table

        else:
            self.engine_request = self.dialect + "://" + self.usr + ":" + self.pwd + "@" + self.url + "/" + self.table

        self.__engine = create_engine(self.engine_request)
        self.__meta = MetaData(self.__engine)
        #self.__tab = Table('test', self.__meta, autoload=True)
        logger.info("DataHandler object initialized")

    def extract_from_table(self, query, **kwargs):
        """
        Method for extracting a request to a pandas dataframe, specifying which column should be used as index
        2015/12/02 : as of now method is hard coded for actual purposes, should be changed
        :param query: A SQL string query
        :return: A pandas dataframe
        """

        if bool(kwargs):

            result = pd.read_sql_query(query, self.__engine)

        else:
            try:

                result = pd.read_sql_query(query, self.__engine, index_col="ID_TICKET")
                logger.info("Loaded RESERVATIONS table successfully")
            except KeyError:

                result = pd.read_sql_query(query, self.__engine, index_col="PK_PRODUITS")
                logger.info("Loaded PRODUCTS table successfully")

        return result

    def write_to_table(self, table):
        """
        Write full table in database
        2015/12/01 : Not in use as of today, may be used for score coefficients or to keep track in time
        :param table: An SQLalchemy Table object
        :return: None
        """

        table.to_sql("test", self.__engine, flavor="mysql", if_exists="replace")

    def exec_request(self, query):
        """
        Method for testing queries, simply executes the argument query
        :param query: a query as string or SQLachemy query object
        :return: None
        """

        self.__engine.execute(query)

    def update_table(self, score_dict):
        """
        Method creates as many thread/request objects as needed and executes them
        :param score_dict: A dict with PRODUCTS ID as keys and computed SCORES as values
        :return: None
        """

        logger.info("Multi-threading sql update tables")

        iterator = score_dict.iterkeys()
        threads = []

        for key in iterator:
            thread = UpdateTable(self.__engine, key, score_dict[key])
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        logger.info("SQL update queries sent and terminated successfully")
