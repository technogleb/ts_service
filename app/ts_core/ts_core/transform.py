from copy import deepcopy
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from scipy.signal import detrend, periodogram
from sklearn.linear_model import LinearRegression


def check_ts(ts):
    """Pre-process TS before taking to detect_ts method
    Makes a copy of ts (in order to prevent changes in original ts).
    Drops NA's, checks wherher all values are numeric, and removes values
    with the same timestamps.
    """
    ts = deepcopy(ts)
    ts.dropna(inplace=True)
    ts = pd.to_numeric(ts)
    ts = ts.loc[~ts.index.duplicated(keep='last')]
    return ts


def get_season_period(ts):
    ts = pd.Series(detrend(ts), ts.index)
    f, Pxx = periodogram(ts)
    Pxx = list(map(lambda x: x.real, Pxx))
    ziped = list(zip(f, Pxx))
    ziped.sort(key=lambda x: x[1])
    highest_freqs = [x[0] for x in ziped[-100:]]
    season_periods = [round(1 / (x + 0.001)) for x in highest_freqs]
    for period in reversed(season_periods):
        if 4 < period < 100:
            return int(period)


def make_index(index):
    """Transforms multiindex into plain index, leaving only first level"""
    if isinstance(index, pd.core.indexes.multi.MultiIndex) and not index.empty:
        idx = pd.DatetimeIndex(list(map(lambda x: x[0], index)))
    elif isinstance(index, pd.core.indexes.range.RangeIndex):
        idx = index
    else:
        idx = pd.to_datetime(index)
    return idx


class TimeSeriesTransformer:
    def __init__(self, num_lags=14):
        self.num_lags = num_lags
        self.season_period = None

    def set_params(self, **parameters):
        for parameter_name, parameter_value in parameters.items():
            setattr(self, parameter_name, parameter_value)

    def get_params(self):
        pass

    def fit(self, ts, y=None, **fit_params):
        self.season_period = get_season_period(ts)
        return self

    def transform(self, ts):
        """
        Takes time-series as an input and returns lag matrix, where features
        are lags. This is used for training purposes.

        Parameters
        ----------
        ts : pd.Series(values, timestamps)
            Time-series to detect on

        Returns
        ---------
        feature_matrix : pd.DataFrame
            Pandas dataframe, which contains feature lags of
            shape(len(ts)-num_lags, num_lags+1)
        """

        ts = check_ts(ts)
        feature_matrix = pd.DataFrame(
            columns=['lag_{}'.format(i) for i in range(1, self.num_lags + 1)] + ['season_lag', 'y']
        )
        feature_matrix['y'] = ts[self.num_lags:]
        for lag in feature_matrix.drop(['y', 'season_lag'], axis=1):
            shift = int(lag.split('lag_')[1])
            feature_matrix[lag] = ts.shift(shift)[self.num_lags:]

        season_period = self.season_period if self.season_period else self.num_lags
        feature_matrix['season_lag'] = ts.shift(season_period)[season_period:]
        feature_matrix.fillna(feature_matrix.mean(), inplace=True)

        return feature_matrix

    def fit_transform(self, ts, y=None, **fit_params):
        return self.fit(ts, y, **fit_params).transform(ts)


class FeatureGenerator:
    def __init__(self):
        pass

    def set_params(self, **parameters):
        for parameter_name, parameter_value in parameters.items():
            setattr(self, parameter_name, parameter_value)

    def get_params(self):
        pass

    def fit(self, feature_matrix, y=None, **fit_params):
        return self

    def transform(self, feature_matrix):
        """
        Takes lag_matrix as input and adds additional features, like datetime info
        and smoothing statistics.

        Parameters
        ----------
        feature_matrix : pd.DataFrame
            Matrix obtained from transform method of TimeSeriesTransformer class

        Returns
        --------
        feature_matrix: pd.DataFrame
            Matrix with additional features
        """

        # datetime features
        lags = [feature for feature in feature_matrix.columns if 'lag_' in feature]
        matrix_index = make_index(feature_matrix.index)
        feature_matrix['weekday'] = list(
            map(lambda x: x.dayofweek, matrix_index))
        feature_matrix['monthday'] = list(
            map(lambda x: x.day, matrix_index))
        feature_matrix['is_weekend'] = feature_matrix['weekday'].apply(
            lambda x: int(x is 0))
        feature_matrix['month'] = list(
            map(lambda x: x.month, matrix_index))
        feature_matrix['hour'] = list(
            map(lambda x: x.hour, matrix_index))
        # static features
        feature_matrix['mean'] = feature_matrix[lags].mean(axis=1)
        feature_matrix['std'] = feature_matrix[lags].std(axis=1) if len(lags) > 1 else 0
        return feature_matrix

    def fit_transform(self, ts, y=None, **fit_params):
        return self.fit(ts, y, **fit_params).transform(ts)
