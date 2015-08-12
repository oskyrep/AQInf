# libs
import pandas as pd;
import numpy as np;
    # linear regression
from scipy import stats;

# Input:
# (a) [float list] feature list 1
# (b) [float list] feature list 2
# Output:
# [numpy matrix] sub Affinity Function matrix after operation

def AffinityFunSubMatrixInit(featureList1, featureList2):

    featureList1 = np.array(featureList1);

    featureList2 = np.array(featureList2).reshape(-1, 1);

    it = np.nditer([featureList1, featureList2, None],
                   [],
                   [['readonly'], ['readonly'], ['writeonly', 'allocate']]);

    subOp = np.subtract;

    for x, y, z in it:
        subOp(x, y, out = z);

    return abs(it.operands[2]);

# Input:
# (a) [float] numpy matrix's entity
# (b) [float] linear function slope
# (c) [float] linear function intercept
# Output:
# [float] new numpy matrix's entity after linearization

def linearizeFun(entity, slope, intercept):
    
    return slope * entity + intercept;

# Input:
# (a) [string list] the node list (labeled + unlabeled)
# (b) [list of dict] the list of labeled node feature dicts ([dict] labeled : feature value)
# (c) [list of dict] the list of unlabeled node feature dicts ([dict] unlabeled : feature value)
# (d) [float] the # of features
# (e) [dict] labeled : AQI
# Output:
# [list of dict] the Affinity Function matrix after initialization

def AffinityFunMatrixListInit(nodeList,
                              labeledFeatureDictList,
                              unlabeledFeatureDictList,
                              numOfFeatures,
                              labeledAQIDict):
    
    tempMatrixList = [0.0] * numOfFeatures;

    # construct labeled AQI array
    # has nothing to do with loops
    AQIList = labeledAQIDict.values();
    labeledAQIDiffArray = np.fabs(AffinityFunSubMatrixInit(AQIList, AQIList)).ravel();

    for i in range(numOfFeatures):

        lList = labeledFeatureDictList[i].values();
        uList = unlabeledFeatureDictList[i].values();
        
        tempMatrix = np.vstack( ( np.hstack([np.fabs(AffinityFunSubMatrixInit(lList, lList)),
                                             np.fabs(AffinityFunSubMatrixInit(uList, lList))]),
                                  np.hstack([np.fabs(AffinityFunSubMatrixInit(lList, uList)),
                                             np.fabs(AffinityFunSubMatrixInit(uList, uList))]) ) );
        
        # get (slope, intercept) from linear regression
        labeledFeatureDiffArray = np.fabs(AffinityFunSubMatrixInit(lList, lList)).ravel();

        # linear regression
        regressResult = stats.linregress(labeledFeatureDiffArray, labeledAQIDiffArray);

        entityLinearizeFun = np.vectorize(linearizeFun, otypes=[np.float]);

        tempMatrix = entityLinearizeFun(tempMatrix, regressResult[0], regressResult[1]);

        tempMatrixList[i] = pd.DataFrame(tempMatrix, index = nodeList, columns = nodeList, dtype = float);

    return tempMatrixList;
