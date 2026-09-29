import itertools
import math
import numpy as np
import pandas as pd
import random

from scipy.stats import skewnorm
# scikit-optimize modules. 
from skopt.sampler import Lhs
from skopt.space.space import Categorical, Integer, Real

def statisticalSampling(variables, n):
    """
    Generate unique parameters for each simulation based on the instructions in the Variables dictionary
    The are several methods which can be used for each parameter.

    discrete: a randomly selected choice from a list
    normal: randomly selected values from a normal/gaussian distribution
    skew: randomly selected values from a skewed normal distribution
    uniform : randomly selct from a uniform distribution
    constant : a repeated constant value

    NOTE: latin hypercube sampling is done in another function
    
    """

    # Initialize a dictionary of parameters
    parameters = {}

    for key, input in variables.items():
        #print (key, input)
        if input["method"] == "discrete":
            v = random.choices(input["values"], k = n)
            parameters[key] = v

        elif input["method"] == "normal":
            v = np.random.normal(input["mu"], input["sigma"], n)
            parameters[key] = v

        elif input["method"] == "skew":
            v = skewnorm.rvs(input["skew"], loc = input["mu"] - input["sigma"], scale = input["sigma"], size = n)
            parameters[key] = v

        elif input["uniform"] == "uniform":
            v = np.random.uniform(min(input["range"]), input["range"], n)
            parameters[key] = v

        elif input["method"] == "constant":
            v = [input["values"]] * n
            parameters[key] = v

    return parameters

def latinHypercubeSampling (variables, n, lhs_type = "classic", criterion = "maximin"):
    """
    Generate unique parameters for each simulation using latin hypercune sampling
    The are several methods which can be used for each parameter.

    discrete/categorical: a randomly selected choice from a list of options
    int: randomly choose an integer from a range
    float: randomly choose a float value from a range
    constant : a repeated constant value

    Return a dataframe of all combinations.

    TODO: Refactor the names
    """
    lhs_instructions = []

    # Iterate through each variable and append the instructions for each variable to lhs_instructions list
    for input in variables.values():

        # categorical and boolean values
        if input["type"] in ["discrete", "constant", "categorical", "bool", bool]:
            lhs_instructions.append(Categorical(input["values"]))

        # numerical values.
        # Be aware that scikit-optimize treats integers different than floats                     
        elif input["type"] in [int, "int"]:
            lhs_instructions.append (Integer(
                min(input["values"]),
                max(input["values"])
            ))
        elif input["type"] in [float, "float"]:
            lhs_instructions.append (Real(
                min(input["values"]),
                max(input["values"])
            ))
        else:
            raise Exception (f"Unsupported input type for latin hypercube sampling: {input['type']}")

    # Create the latin hypercube model instance and generate some values
    lhs = Lhs(lhs_type = lhs_type, criterion = criterion)
    lhs_values = lhs.generate(lhs_instructions, n)
    
    lhs_values = pd.DataFrame(lhs_values, columns = variables.keys())

    return lhs_values

def randomSampling (parameters, n):
    """
    Generate unique parameters for each simulation based on random sampling methods
    The are several methods which can be used for each parameter.

    discrete/categorical: a randomly selected choice from a list of options
    int: randomly choose an integer from a range
    float: randomly choose a float value from a range
    constant : a repeated constant value

    Return a dataframe of all combinations.

    """

    # Initiate a list to store the values
    random_values = []

    # Iterate through each variable and append an array of length n, to the list
    # Depending on the 'type' a different random function will be used
    for k, v in parameters.items():

        if v["type"] in ["discrete", "categorical", "bool", bool]:
            random_values.append(random.choices(v["values"], k = n))

        elif v["type"] in ["constant"]:
                 random_values.append ([v["values"][0]] * n)   


        elif v["type"] in [int, "int"]:
            # Perform an error check if only one value was given. Assume it is like a constant value.
            if len (v["values"]) == 1:
                 random_values.append ([v["values"][0]] * n)  
            # Ensure the given values are in the correct order
            else: 
                min_value = min(v["values"])
                max_value = max(v["values"])

                random_values.append(np.random.randint(
                    min_value,
                    max_value,
                    n
                ))

        elif v["type"] in [float, "float"]:
                # Perform an error check if only one value was given. Assume it is like a constant value.
            if len (v["values"]) == 1:
                 random_values.append ([v["values"][0]] * n)   
            else:
                min_value = min(v["values"])
                max_value = max(v["values"])

                random_values.append(np.random.uniform(
                    min_value,
                    max_value,
                    n
                ))
        else:
            raise Exception (f"Unsupported input type for random sampling: {v['type']}")

    # Convert the list of lists into a dataframe. The transpose function is required to orient them correctly.
    random_values = pd.DataFrame(random_values).T
    random_values.columns = parameters.keys()

    return random_values


def fullFactorialSampling(parameters):
    """ 
    Generate a full-factorial sample based on the parameters given.
    All parameters must be either a constant or categorical datatype otherwise an error will be thrown.

    Returns a dataframe of all combinations.
    """

    # Calculate how many runs will be generated
    n_values = [len(v["values"]) for v in parameters.values()]

    # calculate the factorial
    n_simulations = 1
    for i in n_values:
        n_simulations *= i

    print (f"A total of {n_simulations} will be generated using the full-factorial method.")

    # Generate the full-factorial set using itertools.product
    list_of_values = [v["values"] for v in parameters.values()]

    factorial_values = list(itertools.product(*list_of_values))

    # Place this into a dataframe
    factorial_values = pd.DataFrame(factorial_values, columns = parameters.keys())

    return factorial_values

