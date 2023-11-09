import numpy as np
import pandas as pd

import mcpy


class MPLPlottingHelper:

    @staticmethod
    def plt_errorbar_mcsamples(plot_widget, x_values: pd.Series, y_values: pd.Series,
                               xlable='Wavelength [nm]', ylable='(nm)'):
        x = x_values
        #y_values = y_values
        y = y_values.apply(lambda row: row.mean)
        err = y_values.apply(lambda row: row.uncertainty.ustd)
        plot_widget.ax.clear()
        # Plot the simple line
        plot_widget.ax.errorbar(x, y, err)
        #plot_widget.ax.set_xlim(np.min(data[x_axis]), np.max(data[x_axis]))
        #plot_widget.ax.set_ylim(np.min(data[y_axis]), np.max(data[y_axis]))
        # Scatter plot of the peaks
        plot_widget.ax.set_xlabel(xlable)
        plot_widget.ax.set_ylabel(ylable)
        plot_widget.ax.grid(True)

        plot_widget.canvas.draw()
