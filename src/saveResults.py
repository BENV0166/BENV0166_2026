from pathlib import Path

import pandas as pd


def saveNSGA2History(history, parameters, saveName):
    """
    This function parses through the res.history object and retrieves the design space parameters (X) and objective function values (F) for each individual in each generation and stores them in a pandas dataframe.

    It then saves the results and also returns the history of X and F.
    """

    # Initialize a list of lists for the design and objective spaces
    rows_X = []
    rows_F = []

    # Iterate through the history of each generation and each individual
    for i, generation in enumerate(history):
        for j, individual in enumerate(generation.pop):
            row_X = [i, j] + list(individual.X)
            row_F = [i, j] + list(individual.F)
            rows_X.append(row_X)
            rows_F.append(row_F)

    # Create and save to csv a dataframe for the design space (X)
    columnNames = ["generation", "individual"] + list(parameters.keys())
    history_X = pd.DataFrame(rows_X, columns=columnNames)
    savePath = Path("outputs", "results", f"history_X_{saveName}.csv")
    history_X.to_csv(savePath, index = False)
    print(f"Design space history dataframe saved to {savePath}.")

    # Create and save to csv a dataframe for the design space (F)
    columnNames = ["generation", "individual"] + ["heatingMax", "SET > 30°C Degree-Hours [°C·hr]"]
    history_F = pd.DataFrame(rows_F, columns=columnNames)
    savePath = Path("outputs", "results", f"history_F_{saveName}.csv")
    history_F.to_csv(savePath, index = False)
    print(f"Objective space history dataframe saved to {savePath}.")

    return history_X, history_F


def saveNSGA2Optimal(X, F, n_generations, saveName):
    X["generation"] = n_generations
    savePath = Path("outputs", "results", f"optimalSet_X_{saveName}.csv")
    X.to_csv(savePath, index = False)
    print(f"Design space optimal set dataframe saved to {savePath}.")

    F["generation"] = n_generations
    savePath = Path("outputs", "results", f"optimalSet_F_{saveName}.csv")
    F.to_csv(savePath, index = False)
    print(f"Objective space optimal set dataframe saved to {savePath}.")

    return X, F
