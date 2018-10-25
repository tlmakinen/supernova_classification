"""
Quick script for making latent variable plots for comparing SN smear types
- Requires that you've cleaned your FITRES files into pandas dataframes
- Inputs: 
        smeartype: string name of smear file
        data_all:  bulk data file
        data_sel:  file of selected supernovae

- Returns:
        Plots matplotlib histograms of latent variable distributions
   """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def makeLatentHistograms(smeartype, data_all, data_sel):

    # isolate missed SNe
    selected_mask = data_all['selection_tag'].values.astype(bool)
    missed_mask = np.invert(selected_mask)

    # Let's take a look at the OBSERVED SNe... We're going to "zoom in" on the normally-distributed populations from the plots above

    # define lists of plotting features for latent mB, c, & x1
    sel_names = ["zHEL", "SIM_mB", 'SIM_c', 'SIM_x1']
    obs_names = ["GENZ", 'S2mB', 'S2c', 'S2x1']
    labels = ['$z$', '$m_B$', '$c$', '$x_1$']
    allbinz = [10, 10, 10, 10]
    selbinz = [10, 10, 10, 10]
    missedbinz = [10, 10, 15, 10]
    xlims = [(0, 1.3),(14, 30), (-0.5, 0.5), (-4, 2)]

    # make the plot
    fig,axs = plt.subplots(2, 2, figsize = (9,9))

    # sum number of objects in each category
    selsum = str(len(data_sel))
    observedsum = str(len(data_all))
    missedsum = str(sum(missed_mask))

    # flatten axes list to iterate over them
    axs = np.ravel(axs)

    for i in range(len(axs)):
        # selected Ia SNe
        axs[i].hist(data_sel[sel_names[i]], histtype='step', bins=selbinz[i], color='b', label=selsum +' Selected Ia SNe', stacked=False, density=True)
        # bulk Ia SNe
        axs[i].hist(data_all[obs_names[i]], histtype='step', bins=allbinz[i], color='k', label= observedsum + ' Total Ia SNe', stacked=False, density=True)
        # add missed Ia SNe
        axs[i].hist(data_all[obs_names[i]].iloc[missed_mask], histtype='step', bins=missedbinz[i], color='r', label= missedsum + ' Missed Ia SNe', stacked=False, density=True)
        # plot labels
        axs[i].set_xlabel(labels[i], fontsize=15)
        axs[i].set_xlabel(labels[i], fontsize=15)
    
    #axs[i].set_xlim(xlims[i]|)

    fig.suptitle("Normalized Distributions of {} smear SNIa Latent Variables".format(smeartype[5:]), fontsize=20)
    axs[1].legend(loc='best')
    plt.show()