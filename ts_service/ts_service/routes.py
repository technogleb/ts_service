from flask import current_app as app
from flask import request
from ts_core import TimeSeriesPredictor
import joblib
import pandas as pd


def json2ts(json_data):
    ts = pd.Series()
    for dt, value in json_data.items():
        ts[dt] = value
    return ts


@app.route('/api/train/', methods=['POST'], strict_slashes=False)
def train():
    user_data = request.get_json(force=True)
    ts_id = user_data['key']
    user_ts = json2ts(user_data['points'])
    predictor = TimeSeriesPredictor()
    predictor.fit(user_ts)
    joblib.dump(predictor, f'{ts_id}.pkl')
    joblib.dump(user_ts, f'ts_{ts_id}.pkl')
    return 'Model is succesfully trained'


@app.route('/api/predict_next', methods=['GET'], strict_slashes=False)
def predict():
    user_data = request.get_json(force=True)
    ts_id = user_data['key']
    predictor = joblib.load(f'{ts_id}.pkl')
    ts = joblib.load(f'ts_{ts_id}.pkl')
    value = predictor.predict_next(ts)
    return value.to_json()
