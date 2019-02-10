"""
Routine for logistic regression on SNANA-simulated supernovae using scikit-learn.
Methods include:
- plotSelectionFunction
- generateCoeffs

Inputs: data_all, data_sel

"""

# The modules we're going to need
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
# turn off annoying write warnings
pd.options.mode.chained_assignment = None  # default='warn'

import pylab as pl
import scipy
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import cross_val_score

from patsy import dmatrices  # neat helper module from patsy

def log_indiv_selection_fn(phi_i, selection_param):
    coefs = np.array(selection_param)
    position = np.array([*phi_i, 1])
    argument = np.dot(coefs, position)
    # must be a logcdf so it dies/grows to 0/1 at the right speed
    return scipy.stats.norm.logcdf(np.sqrt(np.pi/8)*argument)

def generateCoeffs(data_all, data_sel):
        # First take a look at regression on the whole dataset
    Z, phi = dmatrices('selection_tag ~ S2mB + S2c + S2x1', data_all, return_type = 'dataframe')
    # define model, and set parameter regularization to a minimum --> WHY??
    log_model = LogisticRegression(fit_intercept = False, C = 1e9)
    Z = np.ravel(Z) # flatten Z to 1D
    mdl = log_model.fit(phi, Z)


    # regression using train and test groups
    # Next, split the observed SNe into two groups:
    # 25% data_train, 75% data_test
    phi_train, phi_test, Z_train, Z_test = train_test_split(phi, Z, train_size=0.25, test_size=0.75, random_state = 0)

    # use limited-memory Broyden-Fletcher-Goldfarb-Shanno algorithm with no parameter regularization
    learn_model = LogisticRegression(fit_intercept = False, C = 1e9, solver='lbfgs') 
    learn_model.fit(phi_train, Z_train)

    # Zip up coeffs to return them
    coeff_table = pd.DataFrame(list(zip(phi.columns, np.transpose(learn_model.coef_))))

    # predict whether a SN in the test set was selected, using our phi_test values
    predicted = learn_model.predict(phi_test)


    # unpack the parameters
    pars = learn_model.coef_[0]
    eps,gm,gc,gx = pars

    # unpack parameters to predict selection probability with the selection function
    phi_test_list = []
    for par in ['S2mB', 'S2c', 'S2x1']:
        phi_test_list.append(np.asarray(phi_test[par]))

    # make predictions using the model and add results to "test" dataframe
    phi_test.loc[:,"selection_prediction"] = pd.Series(np.exp((
                                                log_indiv_selection_fn(phi_test_list, 
                                                                                  selection_param=(gm,gc,gx,eps)))), 
                                                                                                   index=phi_test.index) 
    return phi_test,Z_test,coeff_table


def plotSelectionFunction(smeartype, data_all, data_sel, figpath=None):

    phi_test,Z_test,coeffs = generateCoeffs(data_all,data_sel)

    # Make a nifty plot to show the probability of selection in the test data as a function of one variable:

    fig,axs = plt.subplots(1, 3, figsize = (17,5))
    par_tags = ['S2mB', 'S2c', 'S2x1']
    latent_names = [' $m_B$', ' $c$', ' $x_1$']
    xlims = [(15, 27), (-0.8, 0.8), (-4, 4)]

    # split the selected SNe from the missed SNe
    select_mask_true = Z_test.astype(bool)             # masks of all selected (Z = 1) SNe
    missed_mask_true = np.invert(select_mask_true)     # mask of all missed SNe

    # unpack parameters to plot cross-sections with the selection function
    phi_test_plot = []
    for par in ['S2mB', 'S2c', 'S2x1']:
        phi_test_plot.append(np.asarray(phi_test[par]))

    phi_missed = []
    phi_select = []
    for parameter in phi_test_plot:
        phi_missed.append(parameter[missed_mask_true])
        phi_select.append(parameter[select_mask_true])


    for i in range(len(axs)):
        # plot missed SNe
        axs[i].scatter(phi_test[par_tags[i]].iloc[missed_mask_true][::5], 
                        phi_test['selection_prediction'].iloc[missed_mask_true][::5], 
                                color='r', marker = '.', alpha=1, s=3, label='missed')
        
        # plot selected SNe
        axs[i].scatter(phi_test[par_tags[i]].iloc[select_mask_true][::5], phi_test['selection_prediction'].iloc[select_mask_true][::5], 
                    color='b', marker = '.', alpha=1, s=3, label='selected')
        
        # restrict xlims to observed SNe    
        axs[i].set_xlim(xlims[i])    
        # add labels
        axs[i].set_xlabel(latent_names[i], fontsize=15)
        axs[i].set_ylabel('$P(Z_i=1|$' + latent_names[i] + '$)$', fontsize=15)

    fig.suptitle('Selection Function Classifier on Test {} SNIa set'.format(smeartype[5:]), fontsize=17)
    #plt.legend(loc='best')
    #plt.savefig(fname='/mnt/c/Users/lucas/Documents/Fall2018/Imperial_2018/JP2/plots', dpi='figure')
    plt.show()

    # save figure
    if figpath is not None:
        fig.savefig(figpath, dpi='figure')