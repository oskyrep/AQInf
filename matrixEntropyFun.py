# Input:
# [2D dict of float values] the matrix whose entropy to be calculated
# Output:
# [float] the calculated entropy

# log fun
import math;

def matrixEntropyFun(matrix):
    
    # the # of nodes = the first dim of matrix
    numOfNodes = len(matrix);
    entropy = 0.0;

    for AQILabel in matrix.itervalues():
        for entity in AQILabel.itervalues():
            # if p = 0 or 1: entropy = 0
            if entity > 0.0 and entity < 1.0:
                entropy += entity * math.log(entity, 2) + (1-entity) * math.log(1-entity, 2);

    return (- entropy) / numOfNodes;
