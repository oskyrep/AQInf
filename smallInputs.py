import pandas as pd;
import numpy as np;
import random;

labeledList = ['v1','v2','v3'];
unlabeledList = ['u1','u2','u3','u4','u5'];
timeStampList = ['t1','t2','t3'];
featureList = ['f1','f2','f3'];

labeledAQITable = pd.DataFrame([[123,265,379],
                                [250,300,275],
                                [300,350,325]],
                                index = timeStampList,
                                columns = labeledList);

numToBeRecommend = 3;
                                       
labeledFeatureTimeStampPanel = \
pd.Panel(1000 * np.random.random_sample((len(timeStampList),len(labeledList),len(featureList))) + 0,
         items = timeStampList,
         major_axis = labeledList,
         minor_axis = featureList,
         dtype = float);

unlabeledFeatureTimeStampPanel = \
pd.Panel(1000 * np.random.random_sample((len(timeStampList),len(unlabeledList),len(featureList))) + 0,
         items = timeStampList,
         major_axis = unlabeledList,
         minor_axis = featureList,
         dtype = float);
