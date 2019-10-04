# ```ts-eval``` Time Series analysis and evaluation tools

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pypi](https://img.shields.io/pypi/v/ts-eval)](https://pypi.org/project/ts-eval/)
---
A set of tools to help you analyse time series using Python.

## 🧩 Current features

* N-step ahead evaluation widget for Jupyter
* Absolute & relative metrics for point forecasts and prediction intervals (MSE, MAE, rMSE, rMAE, MIS, rMIS)
* Fixed fourier series generation (fixed in time according to pandas index)
* Naive/Seasonal models for baseline (with prediction intervals)
* Helper functions to evaluate n-step ahead forecasts using Statsmodels models or naive/seasonal naive models.

## 📋 Release Planning:

* Release 0.2
  * fix ipynb nbviewer preview
  * holiday/fourier features model
  * fix viz module to have less of important stuff
  * a gif with project visualization
  * check shapes of input arrays (target vs preds), now it doesn't raise an error
  * Baseline prediction using target dataset (without explicit calculation, but losing some time points)
  * Graph: plot confint
  * Nemenyi
  * Residual stats: since I have residuals => Ljung-Box, Heteroscedasticity test, Jarque-Bera – like in statsmodels results.

## 💡 Ideas

* components
  * Graph: Visualize outliers from confidence interval
  * Multi-comparison component: scikit_posthocs lib or homecooked?
  * inspect true confidence interval coverage via sampling (was done in postings around bayesian dropout sampling)
  * xarrays: compare if compared datasets are actually equal (offets by dates, shapes, maybe even hashing)
  * bin together step performance, like steps 0-1, 2-5, 6-12, 13-24
  * highlight regions using a mask (holidays, etc.)
  * option to view interactively points using widget (plotly)?
  * diagnostics: bias to over / underestimate points
* features
  * example notebook for fourier?
  * tests for fourier
  * nint generation
* utils:
  * model adaptor (for different models, generic) which generates 3d prediction dataset. For stastmodels using dyn forecast or kalman filter
  * future importance calculator, but only if I can manipulate input features
  * feature selection using PACF / prewhiten?
* project
  * more defensive style (add arg checks, so it's easier to understand what is going on)
  * docstrings
  * circleci
  * https://timothycrosley.github.io/portray/ for docs
* sMAPE & MASE can be added for the jupyter evaluation tables
* For multiple comparisons:
    import scikit_posthocs as sp
    sp.posthoc_nemenyi_friedman(pmm)


## 🤹🏼‍♂️ Development

Recommended development workflow:
```
pipenv install -e .[dev]
pipenv shell
```
The library doesn't use Flit/Poetry, so the suggested workflow is based on Pipenv (as per https://github.com/pypa/pipenv/issues/1911).
Pipfile* are ignored in the .gitignore.
