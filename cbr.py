# Import
import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sn

# Main


def cbr_algorithm(cases):
    # [1] Get the input .csv library and problem cases
    library = pd.read_csv(
        'input/library.csv')

    # Select columns from library to use as base cases, except solutions
    # Exclude last column (solution)
    base = library.iloc[:, range(library.shape[1] - 1)]

    # print(f'\n> Base \n{base}')

    # [2] Initial One-hot encoding
    base = pd.get_dummies(base)
    problems = pd.get_dummies(cases)

    # [3] Calculate
    print('\n> Calculating\n')
    caseResult = ''

    # Move through all problem cases
    for i in range(problems.shape[0]):
        # [3.1] Get inverse covariance matrix for the base cases
        covariance_matrix = base.cov()                                      # Covariance
        inverse_covariance_matrix = np.linalg.pinv(
            covariance_matrix)       # Inverse

        # [3.2] Get case row to evaluate
        case_row = problems.loc[i, :]

        # Empty distances array to store mahalanobis distances obtained comparing each library cases
        distances = np.zeros(base.shape[0])

        # [3.3] For each base cases rows
        for j in range(base.shape[0]):
            # Get base case row
            base_row = base.loc[j, :]

            # [3.4] Calculate mahalanobis distance between case row and base cases, and store it
            distances[j] = distance.mahalanobis(
                case_row, base_row, inverse_covariance_matrix)

        # [3.5] Returns the index (row) of the minimum value in distances calculated
        min_distance_row = np.argmin(distances)

        # [4] Get solution based on index of found minimum distance, and append it to main library
        # From cases, append library 'similar' solution
        case = np.append(cases.iloc[i, :], library.iloc[min_distance_row, -1])
        caseResult = case[-1].strip()
        # Print
        print(
            f'> For case/problem {i}: {cases.iloc[i, :].to_numpy()}, solution is {case[-1]}')

        # [5] Store
        # Get as operable pandas Series
        # Case with Solution
        case = pd.Series(case, index=library.columns)
        result = pd.DataFrame()
        result = result.append(
            case, ignore_index=True)
        
        library = library.append(
            case, ignore_index=True)

        # Save 'covariance heat map (biased)' output as file
        sn.heatmap(np.cov(base, bias=True), annot=True, fmt='g')
        plt.gcf().set_size_inches(12, 6)
        plt.title(
            f'Covariance Heat map #{i} \n Library cases stored {j} - Base to solve problem {i}')
        plt.savefig(f'output/covariance_heat_map_{i}.png', bbox_inches='tight')
        plt.close()

        # [6] Reuse
        # Exclude last column (solution)
        base = library.iloc[:, range(library.shape[1] - 1)]
        # Get new one-hot encoded base
        base = pd.get_dummies(base)

    # Save 'library' output as file
    result.to_csv('output/result.csv', index=False)
    library.to_csv('input/library.csv', index=False)
    return caseResult


# Call
if __name__ == '__main__':
    cbr_algorithm()
