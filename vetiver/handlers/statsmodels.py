import pandas as pd

from ..meta import _model_meta
from .base import BaseHandler

sm_exists = True
try:
    import statsmodels
except ImportError:
    sm_exists = False


class StatsmodelsHandler(BaseHandler):
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : statsmodels
        a trained sklearn model
    """

    model_class = staticmethod(
        lambda: statsmodels.regression.linear_model.RegressionResultsWrapper
    )

    def __init__(self, model, ptype_data):
        super().__init__(model, ptype_data)

    def describe(self):
        """Create description for sklearn model"""
        desc = f"Statsmodels {self.model.__class__} model."
        return desc

    def construct_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
        required_pkgs = required_pkgs + ["statsmodels"]
        meta = _model_meta(user, version, url, required_pkgs)

        return meta

    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """

        if check_ptype:
            if isinstance(input_data, pd.DataFrame):
                prediction = self.model.predict(input_data)
            else:
                prediction = self.model.predict([input_data])

        # do not check ptype
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?

            prediction = self.model.predict(input_data)

        return prediction
