import threading

__author__ = "Thomas"


class UpdateTable(threading.Thread):
    """
    Class creating the different threads for updating the database
    Each thread is a single SQL query
    2015/12/01 : As of now the request is static, it should be passed as an argument, and therefore could do more than
                                                                                        just updates
    2015/12/01 : This class should inherit from a broader query class
    """

    def __init__(self, engine, details):
        threading.Thread.__init__(self)
        self.engine = engine
        self.details = details

    def run(self):
        """
        Executes unique request of the object
        :return: None
        """
        var_map = {'builder':"CONSTRUCTEUR", 'Displacement':"DEPLACEMENT", 'Beam':"MAITRE_BAU", 'Length':"LONGUEUR",
            'model':"MODELE" "MODELE", 'type':"TYPE",
            'No. of Beds':"CAPACITE_COUCHAGE", 'Max speed':"VITESSE_MAX", 'Range':"RANGE",
            'Engine':"MOTEUR", 'Cruising speed':"VITESSE_CROISIERE",
            'Length Waterline':"LONGUEUR_LIGNE_FLOTTAISON", 'Depth':"PROFONDEUR",
            'Certified nr. of persons':"CAPACITE_AUTORISEE", 'No. of Cabins':"NOMBRE_CABINE",
            'engine power': "PUISSANCE_MOTEUR"}

        update = "UPDATE PRODUITS SET NOTE_NEW_ALGO = %(value).9f WHERE PK_PRODUITS = %(key)s"%{"value": self.value["SCORE"], "key": self.key}

        self.engine.execute(update)
