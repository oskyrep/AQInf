import pandas as pd;
import numpy as np;
from scipy import stats;

def AffinityFunSubMatrixInit(featureList1, featureList2):

    featureList1 = np.array(featureList1);

    featureList2 = np.array(featureList2).reshape(-1, 1);

    it = np.nditer([featureList1, featureList2, None],
                   [],
                   [['readonly'], ['readonly'], ['writeonly', 'allocate']]);

    subOp = np.subtract;

    for x, y, z in it:
        subOp(x, y, out = z);

    return it.operands[2];

def linearizeFun(entity, slope, intercept):
    
    return slope * entity + intercept;

def AffinityFunMatrixListInit(nodeList, labeledFeatureDictList, unlabeledFeatureDictList, numOfFeatures, labeledAQIDict):
    
    tempMatrixList = [0.0] * numOfFeatures;

    AQIList = labeledAQIDict.values();
    labeledAQIDiffArray = AffinityFunSubMatrixInit(AQIList, AQIList).ravel();

    for i in range(numOfFeatures):

        lList = labeledFeatureDictList[i].values();
        uList = unlabeledFeatureDictList[i].values();
        
        tempMatrix = np.vstack( ( np.hstack([AffinityFunSubMatrixInit(lList,lList),
                                             AffinityFunSubMatrixInit(uList,lList)]),
                                  np.hstack([AffinityFunSubMatrixInit(lList,uList),
                                             AffinityFunSubMatrixInit(uList,uList)]) ) );
        
        # get (slope, intercept) from linear regression
        labeledFeatureDiffArray = AffinityFunSubMatrixInit(lList,lList).ravel();

        regressResult = stats.linregress(labeledFeatureDiffArray, labeledAQIDiffArray);

        entityLinearizeFun = np.vectorize(linearizeFun, otypes=[np.float]);

        tempMatrix = entityLinearizeFun(tempMatrix, regressResult[0], regressResult[1]);

        tempMatrixList[i] = pd.DataFrame(tempMatrix, index = nodeList, columns = nodeList, dtype = float);

    return tempMatrixList;
