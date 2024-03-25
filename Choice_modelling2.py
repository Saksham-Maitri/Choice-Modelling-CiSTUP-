
"""Importing Necessary library"""
import numpy as np


# Data that was provided
data = {
 'X1': [2,1,3,4,2,1,8,7,3,2],
 'X2': [8,7,4,1,4,7,2,2,3,1],
 'Sero': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 "S1": [3,8,4,7,1,6,5,9,2,3],
 "AV1" : [1,1,1,1,1,0,0,1,1,0],
 "AV2": [1,1,1,0,0,1,1,1,0,1],
 "AV3": [1,1,0,0,1,1,1,1,1,1]
}

# Converting all the List(int) into numpy array for better handling
for key,value in data.items():
    data[key]=np.array(value)


"""Parameters that were provided"""
parameters = {
    'beta01': 0.1,
    'beta1': -0.5,
    'beta2': -0.4,
    'beta02': 1,
    'beta03': 0,
    'betaS1_13': 0.33,
    'betaS1_23': 0.58
}

# Deterministic Utilities function that will provide us V1,V2,V3 or return error
def deterministic_utilities(data,parameters):
    """
    we will calculate the utilities according to the given formula. I have added constraints that will make this function return Error detected in any case
    of error
    𝑉1 = 𝛽01 + 𝛽1𝑋1 + 𝛽𝑆1,13𝑆1
    𝑉2 = 𝛽02 + 𝛽2𝑋2 + 𝛽𝑆1,23𝑆1
    𝑉3 = 𝛽03 + 𝛽1𝑆𝑒𝑟𝑜 + 𝛽2𝑆𝑒𝑟𝑜
    """
    if len(data['X1']) != len(data['S1']) or len(data['X2']) != len(data['S1']):
        return "Error detected: Incompatible dimensions for calculation"
    x1_len=len(data['X1'])
    x2_len=len(data['X2'])
    v1 = np.ones(len(data['X1'])) * parameters['beta01'] + parameters['beta1'] * data['X1'] + parameters['betaS1_13'] * data['S1']
    v2 = np.ones(len(data['X2'])) * parameters['beta02'] + parameters['beta2'] * data['X2'] + parameters['betaS1_23'] * data['S1']
    if np.all(data['Sero'] == 0):
        v3 = np.ones(len(data['AV3'])) * parameters['beta03']
    else:
        v3 = np.ones(len(data['Sero'])) * parameters['beta03'] + parameters['beta1'] * data['Sero'] + parameters[
            'beta2'] * data['Sero']

    return {'V1': v1, 'V2': v2, 'V3': v3}


# Using this function , we get are deterministic utilities
utilities=deterministic_utilities(data,parameters)

def calculate_probablities(data,parameters,utilities):
    """
    We will compute the probabilities using the formulae given below. We have used dot product for "*" operation.
    
    Probabilities to Compute:
𝑃1 =
𝐴𝑉1 × 𝑒𝑥𝑝(𝑉1)
𝐴𝑉1 × 𝑒𝑥𝑝(𝑉1) + 𝐴𝑉2 × 𝑒𝑥𝑝(𝑉2) + 𝐴𝑉3 × 𝑒𝑥𝑝(𝑉3)
𝑃2 =
𝐴𝑉2 × 𝑒𝑥𝑝(𝑉2)
𝐴𝑉1 × 𝑒𝑥𝑝(𝑉1) + 𝐴𝑉2 × 𝑒𝑥𝑝(𝑉2) + 𝐴𝑉3 × 𝑒𝑥𝑝(𝑉3)
𝑃1 =
𝐴𝑉3 × 𝑒𝑥𝑝(𝑉3)
𝐴𝑉1 × 𝑒𝑥𝑝(𝑉1) + 𝐴𝑉2 × 𝑒𝑥𝑝(𝑉2) + 𝐴𝑉3 × 𝑒𝑥𝑝(𝑉3)

"""
    if type(utilities)==str:
        return "Error in utilities"

    if len(data['AV1']) != len(utilities['V1']):
        return "Error: Incompatible dimensions between AV1 and V1"
    if  len(data['AV2']) != len(utilities['V2']):
        return "Error: Incompatible dimensions between AV2 and V2"
    if  len(data['AV3']) != len(utilities['V3']):
        return "Error: Incompatible dimensions between AV3 and V3"

    P1 = np.dot(data['AV1'], np.exp(utilities['V1']))
    P2 = np.dot(data['AV2'], np.exp(utilities['V2']))
    P3 = np.dot(data['AV3'], np.exp(utilities['V3']))


    denominator = P1 + P2 + P3


    P1 = P1 / denominator
    P2 = P2 / denominator
    P3 = P3 / denominator


    return {'P1':P1,'P2':P2,'P3':P3}

#Output of the Function 
print("Output is of choice modelling.py is :",calculate_probablities(data,parameters,utilities))

