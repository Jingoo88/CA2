
import log
import threading

__author__ = "Thomas"

logger = log.setup_custom_logger('UpdateTable')


class UpdateTable(threading.Thread):
    """
    Class creating the different threads for updating the database
    Each thread is a single SQL query
    2015/12/01 : As of now the request is static, it should be passed as an argument, and therefore could do more than
                                                                                        just updates
    2015/12/01 : This class should inherit from a broader query class
    """

    def __init__(self, engine, key, value):
        threading.Thread.__init__(self)
        self.engine = engine
        self.key = key
        self.value = value

    def run(self):
        """
        Executes unique request of the object
        :return: None
        """

        update = "UPDATE PRODUITS SET NOTE_NEW_ALGO = %(value).9f WHERE PK_PRODUITS = %(key)s"%{"value": self.value["SCORE"], "key": self.key}

        self.engine.execute(update)
