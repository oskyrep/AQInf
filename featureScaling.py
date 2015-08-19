#!/usr/bin/python

from sklearn import preprocessing;
import pandas as pd;
import numpy as np;

def featureScaling(AffinityFunPanel):
    
    minMaxScaler = preprocessing.MinMaxScaler();

    for feature in AffinityFunPanel.items:
        
        tempMatrix = minMaxScaler.fit_transform(AffinityFunPanel[feature].values);
        AffinityFunPanel[feature] = pd.DataFrame(tempMatrix,
                                                 index = AffinityFunPanel.major_axis,
                                                 columns = AffinityFunPanel.minor_axis,
                                                 dtype = float);

    return AffinityFunPanel;
