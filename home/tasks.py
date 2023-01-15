import random

import requests
from celery import shared_task
import os
import logging
import requests as rq
import time

#import models
from home.models import DataStore
from django.utils.dateparse import parse_datetime

from celery import shared_task
# from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings

MIN_RATE = os.environ.get('BTC_MIN_VAL')
MAX_RATE = os.environ.get('BTC_MAX_VAL')
BTC_FETCH_COINGECKO_URL = os.environ.get('BTC_URL')
TO_MAIL_LIST = os.environ.get('TO_MAIL_LIST').split(',')
FROM_EMAIL = os.environ.get('FROM_EMAIL')

@shared_task
def fetch_btc():
    start_time = time.time()
    logging.info(f"Scheduler Starting for fetching btc data: {start_time}")
    try:
        resp = rq.get(BTC_FETCH_COINGECKO_URL).json()
        if len(resp) != 0:
            for data in resp:
                updated_date = parse_datetime(data.get('last_updated'))
                datastore = DataStore(
                    coin_id = data.get('symbol'),
                    coin_name= data.get('id'),
                    current_price= data.get('current_price'),
                    last_updated = updated_date)
                datastore.save()
                logging.info("Data store saved successfully")

                # Mail send based for current price with threshold
                if int(data.get('current_price')) <= int(MIN_RATE):
                    mail_dict = {
                        'subject': f"Alert! Current Price ${data.get('current_price')} "
                                        f"below threshold: {MIN_RATE}",
                        "message": f"Current Price ${data.get('current_price')} below threshold: {MIN_RATE}"
                    }
                    # Mail send
                    send_mail_func.apply_async(args=[mail_dict])
                elif int(data.get('current_price')) >= int(MAX_RATE):
                    mail_dict = {
                        'subject': f"Alert! Current Price ${data.get('current_price')} "
                                        f"Above threshold: {MAX_RATE}",
                        "message": f"Current Price ${data.get('current_price')} "
                                   f" Above threshold: {MAX_RATE}"
                    }
                    # Mail send
                    send_mail_func.apply_async(args=[mail_dict])
    except Exception as e:
        logging.exception(f" Something went wrong: {str(e)}")
        pass
    end_time = time.time()
    logging.info(f" Scheduler Competed for fetching btc data : \tTime taken: {(end_time-start_time)*10**3:.03f}ms")


@shared_task(bind=True)
def send_mail_func(self, main_dict):
    logging.info("Mail send  started")
    subject = main_dict.get('subject')
    to = TO_MAIL_LIST
    from_email = FROM_EMAIL
    message = get_template('email/email.html').render(main_dict)
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    logging.info("Mail send successfully")