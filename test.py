import numpy as np
from ivirse.common.parameter import ndarrays_to_parameters, parameters_to_ndarrays


array = np.random.rand(1280)

a = ndarrays_to_parameters(array)
# for ndarray in array:
#     print(ndarray)
# print(a)
# print(parameters_to_ndarrays(a))