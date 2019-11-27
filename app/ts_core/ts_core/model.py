import pandas as pd
from datetime import timedelta

from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline


from ts_core.transform import TimeSeriesTransformer, FeatureGenerator


def generate_next_row(ts, num_lags=14, granularity='day'):
    """
    Takes time-series as an input and returns next raw, that is fed to the fitted model,
    when predicting next value.

    Parameters
    ----------
    ts : pd.Series(values, timestamps)
        Time-series to detect on

    num_lags : int, default=14
        Defines the number of lag features

    granularity : str, default='day'
        Defines timedelta of your series

    Returns
    ---------
    feature_matrix : pd.DataFrame
        Pandas dataframe, which contains feature lags of
        shape(1, num_lags)
    """
    delta = timedelta(hours=1) if granularity == 'hour' else timedelta(days=1)
    next_timestamp = pd.to_datetime(ts.index[-1]) + delta
    lag_dict = {'lag_{}'.format(i): [ts[-i]] for i in range(1, num_lags + 1)}
    lag_dict.update({'season_lag': ts[-num_lags]})
    df = pd.DataFrame.from_dict(lag_dict)
    df.index = [next_timestamp]
    return df


class TimeSeriesPredictor:
    def __init__(self, num_lags=14, granularity='day'):
        self.num_lags = num_lags
        self._make_transfomer()
        self.granularity = granularity
        self.model = None

    def _make_transfomer(self):
        return make_pipeline(TimeSeriesTransformer(num_lags=self.num_lags), FeatureGenerator())

    def fit(self, ts, **kwargs):
        transformer = self._make_transfomer()
        train = transformer.transform(ts)
        X, y = train.drop('y', axis=1), train['y']

        model = LinearRegression(**kwargs)
        model.fit(X, y)
        self.model = model

    def predict_batch(self, ts, ts_batch):
        if not self.model:
            raise ValueError('Model is not fitted yet')

        unite_ts = ts.append(ts_batch)

        data_batch = self.transformer.transform(unite_ts)[-len(ts_batch):]
        preds = self.model.predict(data_batch.drop('y', axis=1))

        return pd.Series(index=data_batch.index, data=preds)

    def predict_next(self, ts):
        row = generate_next_row(ts, granularity=self.granularity, num_lags=self.num_lags)
        row = FeatureGenerator().transform(row)
        value = self.model.predict(row)
        return pd.Series(value, index=row.index)
