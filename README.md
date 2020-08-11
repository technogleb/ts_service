# ts_service
Example of building web service serving time-series model inside.

### structure
* ts_core is a stand-alone installable package, that contains source code
for time series prediction model
* ts_service contains simple web app code  

### build and run localy
```
docker build -t ts_service .  
docker run -it -p 80:80 ts_service
```

### API description
* /api/train/  
Allows user send his time series for training and saving data

```
json_payload = {  
    "key": "test_timeseries",  
    "points": {  
        "2019-01-01": 12.9  
        "2019-01-02": 13.6  
        ...  
        "2019-01-30": 12.5  
    }   
}
```

```
response: 200 Ok   
"Model is succesfully trained"
```

* /api/predict/  
Allows user to make one-step-ahead prediction based on key

```
json_payload = {  
    "key": "test_timeseries"  
}  
```

```
response 200 Ok
"{"2019-01-31": 13.6}"
```

### Tech stack
* python3.7 tested
* web framework - flask
* wsgi-compatible app server - guncorn
* ml stack - numpy, pandas, sklearn
* containerization - docker
