# ts_service
Example of building web service serving time-series model inside.

### build and run localy
```
docker build -t ts_service .  
docker run -it -p 80:80 ts_service
```

### API description
* /api/train/

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
response: 200 Ok "Model is succesfully trained"
```

* /api/predict/

```
json_payload = {  
    "key": "test_timeseries"  
}  
```

```
response 200 Ok "{"2019-01-31": 13.6}"
```
