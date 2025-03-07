# vetiver <a href='https://rstudio.github.io/vetiver-python/'><img src='docs/figures/logo.png' align="right" height="139" /></a>

<!-- badges: start -->

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental) [![codecov](https://codecov.io/gh/isabelizimm/vetiver-python/branch/main/graph/badge.svg?token=CW6JHVS6ZX)](https://codecov.io/gh/isabelizimm/vetiver-python)

<!-- badges: end -->

_Vetiver, the oil of tranquility, is used as a stabilizing ingredient in perfumery to preserve more volatile fragrances._

The goal of vetiver is to provide fluent tooling to version, share, deploy, and monitor a trained model. Functions handle both recording and checking the model's input data prototype, and predicting from a remote API endpoint. The vetiver package is extensible, with generics that can support many kinds of models, and available for both Python and R. To learn more about vetiver, see:

- the documentation at <https://vetiver.rstudio.com/>
- the R package at <https://rstudio.github.io/vetiver-r/>

You can use vetiver with:

-   [scikit-learn](https://scikit-learn.org/)
-   [PyTorch](https://pytorch.org/)

## Installation

You can install the released version of vetiver from [PyPI](https://pypi.org/project/vetiver/):

```python
python -m pip install vetiver
```

And the development version from [GitHub](https://github.com/rstudio/vetiver-python) with:

```python
python -m pip install git+https://github.com/rstudio/vetiver-python
```

## Example

A `VetiverModel()` object collects the information needed to store, version, and deploy a trained model.

```python
from vetiver import mock, VetiverModel

X, y = mock.get_mock_data()
model = mock.get_mock_model().fit(X, y)

v = VetiverModel(model, save_ptype=True, ptype_data=X, model_name='mock_model')
```

You can **version** and **share** your `VetiverModel()` by choosing a [pins](https://rstudio.github.io/pins-python/) "board" for it, including a local folder, RStudio Connect, Amazon S3, and more.

```python
from pins import board_temp
from vetiver import vetiver_pin_write

model_board = board_temp(versioned = True, allow_pickle_read = True)
vetiver_pin_write(model_board, v)
```

You can **deploy** your pinned `VetiverModel()` using `VetiverAPI()`, an extension of [FastAPI](https://fastapi.tiangolo.com/).

```python
from vetiver import VetiverAPI
app = VetiverAPI(v, check_ptype = True)
```

To start a server using this object, use `app.run(port = 8080)` or your port of choice.

## Contributing

This project is released with a [Contributor Code of Conduct](https://www.contributor-covenant.org/version/2/1/CODE_OF_CONDUCT.html). By contributing to this project, you agree to abide by its terms.

- For questions and discussions about deploying models, statistical modeling, and machine learning, please [post on RStudio Community](https://community.rstudio.com/new-topic?category_id=15&tags=vetiver,question).

- If you think you have encountered a bug, please [submit an issue](https://github.com/rstudio/vetiver-python/issues).
