# ts_service
Example of building web service serving time-series model inside.

### structure
* ts_core is a stand-alone installable package, that contains source code
for time series prediction model
* ts_service contains simple web app code  

### build and run localy
```
docker build -t ts_service -f docker/Dockerfile .  
docker run -it -p 80:80 ts_service
```

### API description
* /api/train/  
Allows user send his time series for training and saving data

```
json_payload =  {
    "key": "test_timeseries",
    "points": {
        "2019-01-01 00:00:00": 0.0,
        "2019-01-02 00:00:00": 0.09983341664682815,
        "2019-01-03 00:00:00": 0.19866933079506122,
        "2019-01-04 00:00:00": 0.2955202066613396,
        "2019-01-05 00:00:00": 0.3894183423086505,
        "2019-01-06 00:00:00": 0.479425538604203,
        "2019-01-07 00:00:00": 0.5646424733950355,
        "2019-01-08 00:00:00": 0.6442176872376911,
        "2019-01-09 00:00:00": 0.7173560908995228,
        "2019-01-10 00:00:00": 0.7833269096274833,
        "2019-01-11 00:00:00": 0.8414709848078965,
        "2019-01-12 00:00:00": 0.8912073600614354,
        "2019-01-13 00:00:00": 0.9320390859672264,
        "2019-01-14 00:00:00": 0.963558185417193,
        "2019-01-15 00:00:00": 0.9854497299884603,
        "2019-01-16 00:00:00": 0.9974949866040544,
        "2019-01-17 00:00:00": 0.9995736030415051,
        "2019-01-18 00:00:00": 0.9916648104524686,
        "2019-01-19 00:00:00": 0.9738476308781951,
        "2019-01-20 00:00:00": 0.9463000876874145,
        "2019-01-21 00:00:00": 0.9092974268256817,
        "2019-01-22 00:00:00": 0.8632093666488738,
        "2019-01-23 00:00:00": 0.8084964038195901,
        "2019-01-24 00:00:00": 0.74570521217672,
        "2019-01-25 00:00:00": 0.6754631805511506,
        "2019-01-26 00:00:00": 0.5984721441039564,
        "2019-01-27 00:00:00": 0.5155013718214642,
        "2019-01-28 00:00:00": 0.4273798802338298,
        "2019-01-29 00:00:00": 0.33498815015590466,
        "2019-01-30 00:00:00": 0.23924932921398198
    }
}
```

```
response: 200 Ok   
"Model is succesfully trained"
```

* /api/predict_next/  
Allows user to make one-step-ahead prediction based on key

```
json_payload = {  
    "key": "test_timeseries"  
}  
```

```
response 200 Ok
{"2019-01-31 00:00:00": 0.1411200081}
```

### Tech stack
* python3.7 tested
* web framework - flask
* wsgi-compatible app server - guncorn
* ml stack - numpy, pandas, sklearn
* containerization - docker
