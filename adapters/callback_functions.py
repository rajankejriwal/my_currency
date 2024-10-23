import datetime
import decimal
import json
import random
import requests

from urllib import parse
from django.conf import settings


def get_timeseries_data_currency_beacon(kwargs):
    """Function to get timeseries data from currency beacon"""
    api_key = settings.CURRENCY_BEANCON_API_KEY
    params = parse.urlencode(
        {
            "api_key": api_key,
            "base": kwargs["source_curr"],
            "start_date": kwargs["start_date"],
            "end_date": kwargs["end_date"],
        }
    )
    url = "{}?{}".format(settings.CURRENCY_BEANCON_TIMESERIES_API, params)
    req = requests.get(url)

    if req.status_code != 200:
        return {"error": True, "msg": str(req.content.decode("utf-8")), "data": []}

    data = json.loads(req.content.decode("utf-8"))["response"]
    final_data = {}

    for keys in data.keys():
        obj = data[keys]
        inner_data_obj = {}

        for inner_keys in obj.keys():
            if inner_keys in settings.CURRENCIES_LIST:
                inner_data_obj.update({inner_keys: obj[inner_keys]})

        final_data.update({keys: inner_data_obj})

    return {"error": False, "msg": "", "data": final_data}


def get_converter_data_currency_beacon(kwargs):
    """Function to get timeseries data from currency beacon"""
    api_key = settings.CURRENCY_BEANCON_API_KEY
    params = parse.urlencode(
        {
            "api_key": api_key,
            "from": kwargs["source_curr"],
            "to": kwargs["exchange_curr"],
            "amount": kwargs["amount"],
        }
    )
    url = "{}?{}".format(settings.CURRENCY_BEANCON_CONVERTER_API, params)
    req = requests.get(url)

    if req.status_code != 200:
        return {"error": True, "msg": str(req.content.decode("utf-8")), "data": []}

    data = json.loads(req.content.decode("utf-8"))["response"]
    return {"error": False, "msg": "", "data": data}


def get_timeseries_data_mock(kwargs):
    """
    Function to generate mock timeseries data
    """
    start_date = datetime.datetime.strptime(kwargs["start_date"], "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(kwargs["end_date"], "%Y-%m-%d").date()
    base = kwargs["source_curr"]
    available_currency_lst = settings.CURRENCIES_LIST

    data = {}

    date_range_lst = [
        start_date + datetime.timedelta(days=x)
        for x in range((end_date - start_date).days + 1)
    ]

    for date in date_range_lst:
        date = str(date)
        data.update({date: {}})
        for currency in available_currency_lst:
            data[date].update(
                {currency: float(decimal.Decimal(random.randrange(1, 1000)) / 100)}
            )

    return {"error": False, "msg": "", "data": data}


def get_converter_data_mock(kwargs):
    """
    Function to generate mock converter data
    """
    return {
        "error": False,
        "msg": "",
        "data": {
            "value": float(decimal.Decimal(random.randrange(1, 1000)) / 100),
        },
    }
