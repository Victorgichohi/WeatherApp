# WeatherApp
A django api that gets the minimum, maximum, average and median temperature for a
given city and period of time.

# Prerequisite
Create an account on https://www.weatherapi.com/ and get the api key. 

## System requirements

```buildoutcfg
Python 3.6 +
```

## Set up
Create your virtual environment and install packages
```buildoutcfg
virtual .env
source .env/bin/activate
pip install -r requirements.txt
```

Run migrations
```buildoutcfg
python manage.py migrate
```

update your environment variables with production api key from weather api - https://www.weatherapi.com/

```buildoutcfg
export WEATHER_API_KEY = "your_api_key"
```

## Run server
```python
python manage.py runserver
```

## Getting weather info
Visit this endpoint from your browser - http://127.0.0.1:8000/api/location/{city}/?days={days}