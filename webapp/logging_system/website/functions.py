import numpy as np


# NumPy arrays and lists
def numpy_array_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [numpy_array_to_list(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: numpy_array_to_list(value) for key, value in obj.items()}
    else:
        return obj

def list_to_numpy_array(obj):
    if isinstance(obj, list):
        return np.array([list_to_numpy_array(item) for item in obj])
    else:
        return obj