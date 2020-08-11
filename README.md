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
&nbsp;&nbsp;&nbsp;&nbsp;"key": "test_timeseries",  
&nbsp;&nbsp;&nbsp;&nbsp;"points": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"2019-01-01": 12.9  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"2019-01-02": 13.6  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"2019-01-30": 12.5  
&nbsp;&nbsp;&nbsp;&nbsp;}   
}
```

```
response: 200 Ok "Model is succesfully trained"
```

* /api/predict/

```
json_payload = {  
&nbsp;&nbsp;&nbsp;&nbsp;"key": "test_timeseries"  
}  
```

```
response 200 Ok "{"2019-01-31": 13.6}"
```
