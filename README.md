# Coingecko 

REST API app that continuously monitors the price of Bitcoin using a third-party API and alert a given email when the price either goes above or below given limits.

- Django (4.0) & DRP : API 
- Celery             : Scheduler
- MailTrap           : SMTP [Notify]

## Features
- Continuesly monitoring `btc` price changing using  coingecko api
- Email Alerting if price cross/reach the threshold set it in the envornment
- Provides API to read the stored value for the `btc` as per the date on query params

### Run with docker
```
git clone https://github.com/renjithsraj/coingecko_wrapper.git 
docker-compose up 
``` 

### Run without Docker
```
Terminal - 1
1. Make sure redis installed in your system
brew install redis(mac)

2. git clone https://github.com/renjithsraj/coingecko_wrapper.git 
cd coingecko_wrapper
Create virtualenv (python version 3.10.2)
pip install -r requirements.txt

3. Run Project
python manage.py runserver
```

#### Enbaling Scheduler
```
cd coingecko_wrapper
vi global.env

# Update below variables

BTC_MIN_VAL = 1 (MIN Threshold)
BTC_MAX_VAL = 2 (Max Threshold)
EMAIL_HOST = smtp.mailtrap.io
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 2525
TO_MAIL_LIST = "<email1>, <email2>" [Comma Seperated string]
FROM_EMAIL = "<email>"

Terminal 2
2. Start redis
redis-server

Terminal 3
3. celery worker start
cd coingecko_wrapper
activate virtual environment

celery -A coingecko_wrapper worker --beat -l info
```

### API Details

- API: `http://127.0.0.1:8000/api/prices/btc?date=29-03-2022&offset=0&limit=100`
- Method: GET
- Response Type:  JSON
- date [Mandatatory]

### Demo

URL : `http://127.0.0.1:8000/api/prices/btc?date=15-01-2023&offset=0&limit=30`
response

```
api/prices/btc?date=15-01-2023&offset=0&limit=10
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "url": "http://127.0.0.1:8000/api/prices/btc?date=15-01-2023&offset=0&limit=2",
    "next": "http://127.0.0.1:8000/api/prices/btc?date=15-01-2023&limit=2&offset=2",
    "count": 67,
    "data": [
        {
            "timestamp": "1673777849",
            "price": "20780.0000",
            "coin": "btc"
        },
        {
            "timestamp": "1673777849",
            "price": "20780.0000",
            "coin": "btc"
        }
        
    ]
}
```



