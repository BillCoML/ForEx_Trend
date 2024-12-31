
import numpy as np

def recode_low_high(array, x1, x2):

    '''
    THis function only recodes values into 7 codes
    '''
    arr = np.abs(array)

    conditions = [
        arr == 0,
        (arr > 0) & (arr <= x1),
        (arr > x1) & (arr <= x2),
        arr > x2
    ]

    # Define the corresponding values for each condition
    values = [0, 1, 2, 3]

    # Apply np.select to assign values based on conditions
    result = np.select(conditions, values)

    return result.astype('int8')

def recode_close(array, x1, x2):

    '''
    THis function only recodes values into 7 codes
    '''

    conditions = [
        array < -x2,
        (array >= -x2) & (array < -x1),
        (array >= -x1) & (array < 0),
        array == 0,
        (array > 0) & (array <= x1),
        (array > x1) & (array <= x2),
        array > x2
    ]

    # Define the corresponding values for each condition
    values = [0, 1, 2, 3, 4, 5, 6]

    # Apply np.select to assign values based on conditions
    result = np.select(conditions, values)

    return result.astype('int8')