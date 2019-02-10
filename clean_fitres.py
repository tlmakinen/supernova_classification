# read in FITRES files and isolate Type Ia SNe
# In-depth analysis done in "selection_function.ipynb"
import pandas as pd
import numpy as np

def makeMLDataframes(smearname):
        # selected SNe
    data_sel = pd.read_csv('/mnt/c/Users/lucas/Datasets/bahamas/selection_fitting/{}/FITOPT001_selected.FITRES'.format(smearname), sep='\s+')
    # bulk SNe
    data_all = pd.read_csv('/mnt/c/Users/lucas/Datasets/bahamas/selection_fitting/{}/SIMGEN_bulk.DAT'.format(smearname), sep='\s+') # bulk simulated SNe

    # convert simulated x0 to mB
    S2mB = [(-2.5 * np.log10(x0) + 10.6) for x0 in data_all['S2x0']]
    data_all.loc[:,'S2mB'] = pd.Series(data=S2mB, index=data_all.index)
    
    # remove nan values to be able to work with the data
    data_all.replace([np.inf, -np.inf], np.nan)
    data_all = data_all.dropna(axis=0,how='any')

    # add tag to bulk file for whether SN selected or not
    intersect = np.intersect1d((data_all['CID']).astype(int), (data_sel['CID']))
    selectIDs = []
    for name in data_all['CID'].astype(int):
        if name in intersect:
            selectIDs.append(1) 
        else:
            selectIDs.append(0)


    # add to Pandas table data_all:
    data_all.loc[:,'selection_tag'] = pd.Series(data=selectIDs, index=data_all.index)
    # convert redshift values from string to floats in data_all
    data_all.loc[:,'GENZ'] = data_all['GENZ'].astype(float)

    # all non-Ia SNe are labeled with a string ID > 0. Let's create a boolean mask to remove them
    snia_mask = np.invert((data_all['NON1A_INDEX'].values.astype(int) > 0).astype(bool))
    # rewrite bulk dataset for just snia
    data_all = data_all.iloc[snia_mask]

    # remove -9 placeholder valued SNe in selection file
    snia_sel = data_sel['SIM_c'].values.astype(int) > -9
    snia_sel &= data_sel['SIM_mB'].values.astype(int) > 0
    snia_sel &= data_sel['SIM_x1'].values.astype(int) > -9
    data_sel = data_sel.iloc[snia_sel]     # re-write the selected dataframe for viable SNIa

    return data_all,data_sel