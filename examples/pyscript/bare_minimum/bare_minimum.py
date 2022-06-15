#!pyscript

import numpy as np
from matplotlib import pyplot as plt
from radiant.server import RadiantAPI
import js

# try:
# import radiant.ps_init
# except:
# pass

########################################################################
class BareMinimum(RadiantAPI):

    # ----------------------------------------------------------------------
    def __init__(self):
        print('Hola mundo')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = np.linspace(0, 10, 1000)
        y = np.sin(x)

        ax.plot(x, y)

        js.document.body.prepend(self.fig2img(fig))


if __name__ == '__main__':
    BareMinimum()
