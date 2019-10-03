import numpy as np

from ts_eval.models.naive import naive_pi, snaive_pi

from .base import ForecastStrategy


class BaseNaiveForecastStrategy(ForecastStrategy):
    naive_fn = None

    def __init__(self, train_endog, train_test_split_index, freq=7, cl=95):
        self.endog = train_endog
        self.train_test_split_index = train_test_split_index
        self.freq = freq
        self.cl = cl

    def forecast(self, h, omit_last_horizon=True):
        preds_batched = []

        ht = h if omit_last_horizon else 0

        for i in range(self.endog.shape[0] - self.train_test_split_index - ht):
            slice_ = self.endog[: self.train_test_split_index + i]
            fc, ub, lb = self.naive_fn(slice_, freq=self.freq, h=h, cl=self.cl)
            preds_batched += [np.stack([ub, fc, lb], 1)]

        return np.stack(preds_batched, 0)


class NaiveForecastStrategy(BaseNaiveForecastStrategy):
    """
    Naive forecast sliding stragegy
    """

    naive_fn = staticmethod(naive_pi)


class SNaiveForecastStrategy(BaseNaiveForecastStrategy):
    """
    Seasonal Naive forecast sliding stragegy
    """

    naive_fn = staticmethod(snaive_pi)
