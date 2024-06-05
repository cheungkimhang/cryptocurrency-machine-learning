import numpy as np
from sklearn.metrics import mean_squared_error

class score:
    def __init__(self):
        pass

    def sharpe_ratio(self, data_list):
        SR = (252 ** 0.5) * np.mean(data_list) / np.std(data_list)
        return SR

    def rmse(self, pred, actual):
        pred = pred[actual.nonzero()].flatten()
        actual = actual[actual.nonzero()].flatten()
        return np.sqrt(mean_squared_error(pred, actual))

