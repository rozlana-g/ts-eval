from collections import OrderedDict

from . import time_slices as default_time_slices
from .components.dataset_description import DatasetDescriptionComponent
from .components.metrics import MetricsComponent
from .components.prediction_plot import PredictionPlotComponent
from .data_containers import xr_2d_factory, xr_3d_factory
from .layouts.jupyter_html import JupyterHTMLLayout


class TSMetrics(object):
    """
    Builder interface for merics components
    """

    def __init__(self, target, *preds, layout_class=JupyterHTMLLayout):
        self._target = target
        self._preds = preds
        self._ref = None
        self._layout_class = layout_class

        # default points of interest: first and last. Motivation: horizons can be quite big, we don't want to
        # draw too many graphs without explicit permission
        self.h = self._target.sizes["h"]
        self._points = [0, self.h - 1] if self.h > 2 else 0
        self._time_slices = [default_time_slices.all]
        self._components = OrderedDict()

        # TODO: settable with methods
        self._names = list(range(len(self._preds)))

    def _register_component(self, key, comp):
        if key in self._components:
            raise Exception(f"Component {key} already registered")
        self._components[key] = comp

    def use_reference(self, ref):
        """
        Sets the base model predictions for relative metrics (typically naive/snaive)
        """
        self._ref = ref
        return self

    def for_horizons(self, *points):
        """
        Sets horizons to display
        """
        assert all(
            [p >= 0 and p < self.h for p in points]
        ), f"Points of interest should be within 0 and {self.h-1}"

        self._points = points
        return self

    def for_time_slices(self, *time_slices):
        """
        Sets time time_slices we want to get merics for. Example: all, weekends, weekdays, holidays, etc.
        """
        # TODO: what do I do if it's defined last, not first? Other methods will not pick it up
        self._time_slices = time_slices
        return self

    def with_description(self):
        self._register_component(
            "description",
            DatasetDescriptionComponent(
                target=self._target,
                pred=self._preds,
                points=self._points,
                time_slice=None,
            ),
        )

        return self

    def with_metrics(self, *metrics):
        # TODO: assert metrics exist or callable
        # TODO: assert point metrics available for this container
        for i, d in enumerate(self._preds):
            for s in self._time_slices:
                self._register_component(
                    f"metrics_{i}_{s.name}",
                    MetricsComponent(
                        target=self._target,
                        pred=d,
                        points=self._points,
                        time_slice=s,
                        reference_pred=self._ref,
                        name=self._names[i],
                        metrics=metrics,
                    ),
                )

        return self

    def with_predictions_plot(self, figsize=(14, 7)):
        self._register_component(
            "prediction_plot",
            PredictionPlotComponent(
                target=self._target,
                preds=self._preds,
                points=self._points,
                time_slices=self._time_slices,
                names=self._names,
                figsize=figsize,
            ),
        )

        return self

    def show(self):
        self.compute()  # this could be more elegant...
        return self._layout_class(self._components)

    def compute(self):
        res = {}
        for k, c in self._components.items():
            c_result = c.compute()
            if c_result:
                res[k] = c_result

        return type("TSMetricsRes", (), res)


def ts_inspect_2d(target, *preds, start_date=None, freq=None):
    """
    Builds TSMertics for point predictions only, creating internal representation for it.
    """
    return TSMetrics(
        xr_2d_factory(target, start_date=start_date, freq=freq),
        *[xr_2d_factory(p, start_date=start_date, freq=freq) for p in preds],
    )


def ts_inspect_3d(target, *preds, start_date=None, freq=None):
    """
    Builds TSMertics for point predictions and prediction intervals, creating internal representation for it.
    """
    return TSMetrics(
        xr_2d_factory(target, start_date=start_date, freq=freq),
        *[xr_3d_factory(p, start_date=start_date, freq=freq) for p in preds],
    )
