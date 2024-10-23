from exchange_rate.models import Currency


def format_db_data(data_lst):
    """Function to format db data"""
    result_dct = {}

    currency_objs = Currency.objects.filter(is_deleted=False).values("id", "code")
    currency_objs = {obj["id"]: obj["code"] for obj in currency_objs}

    # breakpoint()

    for obj in data_lst:
        valuation_date = str(obj.pop("valuation_date"))

        obj = {currency_objs[obj["exchanged_currency"]]: str(obj["rate_value"])}

        if valuation_date not in result_dct:
            result_dct.update({valuation_date: obj})
        else:
            result_dct[valuation_date].update(obj)

    return result_dct
