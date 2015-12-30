
    @staticmethod
    def distance_to_column(x, y, method="Euclide"):

        # assert method is valid
        # deprecated as of today

        assert(type(y) == pd.core.series.Series), "ONE OR BOTH VECTORS IS NOT A PANDA SERIES"
        assert(type(x) == pd.core.series.Series), "ONE OR BOTH VECTORS IS NOT A PANDA SERIES"

        if method == "Euclide":
            result = (x-y)**2

        else:
            result = 0

        return result

    @staticmethod
    def distance_to_value(x, y, method="Euclide"):

        # assert method is valid
        # deprecated as of today

        if type(x) == pd.core.series.Series:
            y = np.float32(y)
            assert(type(y) == np.float32), "NON PANDAS SERIES ARGUMENT MUST BE CONVERTIBLE TO FLOAT"
            if method == "Euclide":
                result = (x-y)**2

        elif type(y) == pd.core.series.Series:
            x = np.float32(x)
            assert(type(x) == np.float32), "NON PANDAS SERIES ARGUMENT MUST BE CONVERTIBLE TO FLOAT"
            if method == "Euclide":
                result = (y-x)**2

        else:
            sys.exit("ONE ARGUMENT MUST BE A PANDAS SERIES")

        return result

    def ols_estimation(self):

        # ols estimation
        # not in use as of today

        self.data["ANNEE_CONSTRUCTION_AGREGE"] = pd.Categorical(self.data.ANNEE_CONSTRUCTION_AGREGE).codes
        X = self.data[["PUISSANCE", "NB_RESERVATIONS_DATE_TICKET", "NB_INTERLOCUTEURS_DATE_TICKET","ANNEE_CONSTRUCTION_AGREGE"]]
        Y = self.data["PRIX_PONDERE"]

        X = sm.add_constant(X)

        self.ols = smf.ols(formula="PRIX_PONDERE ~ C(ANNEE_CONSTRUCTION_AGREGE)", data=self.data).fit()

        print self.ols.summary()