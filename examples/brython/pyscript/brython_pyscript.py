#!brython

from radiant.server import RadiantAPI, pyscript
from browser import document, html


########################################################################
class BareMinimum(RadiantAPI):

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        document.select_one('body') <= html.H1('Radiant-Framework')

        document.select_one('body') <= html.DIV(id='mpl')
        self.plot_sin(f=5)

        document.select_one('body') <= self.plot_sinc(f=1)

    # ----------------------------------------------------------------------
    @pyscript(output='mpl')
    def plot_sin(self, f=10):
        """"""
        import numpy as np
        from matplotlib import pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.linspace(0, 1, 1000)
        y = np.sin(2 * np.pi * f * x)
        ax.plot(x, y)

        return fig

    # ----------------------------------------------------------------------
    @pyscript()
    def plot_sinc(self, f):
        """"""
        import numpy as np
        from matplotlib import pyplot as plt

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.linspace(0, 10, 1000)
        y = np.sin(2 * np.pi * f * x)
        ax.plot(x, y, color='C1')

        return fig


if __name__ == '__main__':
    BareMinimum()
