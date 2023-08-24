from functools import reduce
from typing import List, Tuple

import numpy as np

from ivirse.common import NDArrays, NDArray


def aggregate(results: List[Tuple[NDArrays, int]]) -> NDArrays:
    """Compute weighted average"""
    # Calculate the total number of examples used during training
    num_examples_total = sum([num_examples for _, num_examples in results])
    
    
    # Create a list of weights, each multipled by the related number of examples
    weighted_weights = [
        [layer * num_examples for layer in weights] for weights, num_examples in results
    ] 
    
    # COmpute average weights of each layer
    weights_prime: NDArrays = [
        reduce(np.add, layer_updates) / num_examples_total
        for layer_updates in zip(*weighted_weights)
    ]
    return weights_prime
    
def aggregate_median(results: List[NDArrays]) -> NDArrays:
    """Compute median."""
    
    # Compute median weight of each layer
    median_w: NDArrays = [
        np.median(np.asarray(layer), axis=0) for layer in zip(*results)
    ]
    return median_w