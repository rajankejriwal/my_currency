import datetime

from adapters.models import Provider
from adapters.callback_functions import *
from exchange_rate.models import Currency


def get_exchange_rate_data(
    source_curr,
    valuation_date,
    provider_name,
    operations,
    exchange_curr=None,
    start_date=None,
    end_date=None,
    amount=None,
):
    """
    Function to get the exchange rate details from the provided args.

    Args:
        source_curr - currency code
        exchange_curr - currency code / optional
        valuation_date - valide date upto present date, format - YYYY-mm-dd
        provider_name - name of the provider
        operations - type of operation we are perfoming
        start_date - valide date upto present date, format - YYYY-mm-dd / optional
        end_date - valide date upto present date, format - YYYY-mm-dd / optional
        amount - valide positive integer / optional
    """
    # check if the valuation_date is valid or not
    current_date = datetime.datetime.now().date()
    try:
        converted_val_date = datetime.datetime.strptime(
            valuation_date, "%Y-%m-%d"
        ).date()
    except Exception as e:
        return {
            "error": True,
            "msg": "invalid valuation_date format",
            "data": "",
        }

    if converted_val_date > current_date:
        return {
            "error": True,
            "msg": "invalid valuation_date, date should be less than or equal to present date",
            "data": "",
        }

    if amount and amount <= 0:
        return {
            "error": True,
            "msg": "invalid amount provided",
            "data": "",
        }

    # check for start_date and end_date if provided
    if start_date and end_date:
        try:
            converted_start_date = datetime.datetime.strptime(
                start_date, "%Y-%m-%d"
            ).date()
            converted_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception as e:
            return {
                "error": True,
                "msg": "invalid start_date or end_date format",
                "data": "",
            }

        if converted_start_date > current_date:
            return {
                "error": True,
                "msg": "invalid start_date, date should be less than or equal to present date",
                "data": "",
            }

        if converted_end_date > current_date:
            return {
                "error": True,
                "msg": "invalid start_date, date should be less than or equal to present date",
                "data": "",
            }

        if converted_end_date < converted_start_date:
            return {
                "error": True,
                "msg": "invalid end_date, end_date should be greater than or equal to start_date",
                "data": "",
            }

    # check for valid operations
    if operations not in ["timeseries", "converter"]:
        return {
            "error": True,
            "msg": "invalid operations, operations must be in [timeseries, converter, latest]",
            "data": "",
        }

    # checking if the provided currencies is valid or not
    try:
        Currency.objects.get(code=source_curr, is_deleted=False)

        if exchange_curr:
            Currency.objects.get(code=exchange_curr, is_deleted=False)

    except Exception as e:
        return {
            "error": True,
            "msg": "invalid currency code, please check the source_curr or exchange_curr",
            "data": "",
        }

    # check for valide provider name
    # if there is no valid provider name then it will get the highest priority
    # provider
    provider_obj = (
        Provider.objects.filter(
            name=provider_name,
            is_active=True,
            is_deleted=False,
        )
        .values()
        .first()
    )

    provider_obj_lst = list(
        Provider.objects.filter(
            is_deleted=False,
            is_active=True,
        )
        .order_by("priority")
        .values()
    )

    provider_obj = None

    kwargs = {
        "source_curr": source_curr,
        "valuation_date": valuation_date,
        "provider_name": provider_name,
        "operations": operations,
        "exchange_curr": exchange_curr,
        "start_date": start_date,
        "end_date": end_date,
        "amount": amount,
    }

    # taking the first provider obj, if it returns error then go for next provider
    while True:
        if not provider_obj_lst:
            break

        if not provider_obj:
            provider_obj = provider_obj_lst.pop(0)

        # calling the provider
        function_name = provider_obj["meta_data"][operations]
        result = globals()[function_name](kwargs)

        if not result["error"]:
            return result

        provider_obj = None

    return result
