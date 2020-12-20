# Monteo-Carlo simulation for STOIIP
import numpy as np
import matplotlib.pyplot as plt

class STOIIP:
    """ It will calculate STOIIP """

    def __init__(self, GRV, NTG, fi, Sw, Bo):
        self.GRV = GRV  #Gros Rock Volume
        self.fi = fi    # Porosity
        self.NTG = NTG  # Net To Gross
        self.Sw = Sw    # Saturation of Water
        self.Bo = Bo    # Oil Formation Volume Factor

        # calculate STOIIP.
        self._calc_()

    def _calc_(self):
        """ calculate STOIIP value """
        self.STOIIP = 7750 * (self.GRV*self.NTG*self.fi*(1- self.Sw) )/self.Bo
        return self.STOIIP

class MCS:
    """ Monteo-Carlo simulation """

    def __init__(self, minimum=[], maximum=[]):
        self.minimum = minimum # minimum value for [GRV, NTG, fi, Sw, Bo]
        self.maximum = maximum # maximum value for [GRV, NTG, fi, Sw, Bo]


    def _random_(self, iteration = 1000000):
        """ Gives set of numbers  """
        return np.random.uniform(0,1,iteration)

    def _make_values_(self):
        """ calculates random values for [GRV, NTG, fi, Sw, Bo] """

        self.GRV = self.minimum[0] + self._random_()*(self.maximum[0]-self.minimum[0])
        self.NTG = self.minimum[1] + self._random_()*(self.maximum[1]-self.minimum[1])
        self.fi = self.minimum[2] + self._random_()*(self.maximum[2]-self.minimum[2])
        self.Sw = self.minimum[3] + self._random_()*(self.maximum[3]-self.minimum[3])
        self.Bo = self.minimum[4] + self._random_()*(self.maximum[4]-self.minimum[4])

    def _calc_(self):
        """ calculate STOIIP value MMSTB"""
        # self.STOIIP = 6.29 * 10**(-6) * (self.GRV*self.NTG*self.fi*(1- self.Sw) )/self.Bo
        stoiip = STOIIP(self.GRV, self.NTG, self.fi, self.Sw, self.Bo)
        self.STOIIP = stoiip._calc_()

    def _probability_(self):
        p0 = min(self.STOIIP)
        p10 = np.percentile(self.STOIIP, 10, interpolation='midpoint')
        p50 = np.percentile(self.STOIIP, 50, interpolation='midpoint')
        p90 = np.percentile(self.STOIIP, 90, interpolation='midpoint')
        p100 = max(self.STOIIP)

        self.pX = [p0, p10, p50, p90, p100]
        self.y  = [100, 90, 50, 10, 0]


    def _plot_(self):

        self._random_(1000000)
        self._make_values_()
        self._calc_()
        self._probability_()

        plt.plot(self.pX, self.y, '-ro')
        plt.annotate(f"{round(self.pX[-1])}MMSTB", (self.pX[-1], self.y[-1]))
        plt.annotate(f"P10 - {round(self.pX[-2])}MMSTB", (self.pX[-2], self.y[-2]))
        plt.annotate(f"P50 - {round(self.pX[-3])}MMSTB", (self.pX[-3], self.y[-3]))
        plt.annotate(f"P90 - {round(self.pX[-4])}MMSTB", (self.pX[-4], self.y[-4]))
        plt.annotate(f"{round(self.pX[0])}MMSTB", (self.pX[0], self.y[0]))
        plt.show()


if __name__ == '__main__':
    # [GRV, NTG, fi, Sw, Bo]

    # North Compartment
    maximum_NC = [191998.69, 0.69, 0.24,  0.24, 1.40]
    minimum_NC = [173713.10, 0.62, 0.22, 0.22, 1.32]
    mcs_NC = MCS(minimum_NC, maximum_NC)
    mcs_NC._plot_()
    
    # South Compartment
    maximum_SC = [1035732.02,  0.89, 0.25, 0.26, 1.40]
    minimum_SC = [937090.8755, 0.80, 0.22, 0.23, 1.32 ]
    mcs_SC = MCS(minimum_SC, maximum_SC)
    mcs_SC._plot_()
    


