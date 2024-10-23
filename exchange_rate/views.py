import datetime

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from adapters.utils import get_exchange_rate_data
from exchange_rate.models import Currency, CurrencyExchangeRate
from exchange_rate.utils import format_db_data
from exchange_rate.serializers import CurrencySerializer


class CurrencyListApi(views.APIView):
    """
    This class is used to get the list of rate values for each available
    currency in a time series

    Args:-
        source_currency - Base currency code
        date_from - valid date format - YYYY-mm-dd
        date_to - valid date format - YYYY-mm-dd
    """

    def get(self, request, *args, **kwargs):
        source_curr = self.request.query_params.get("source_currency", None)
        start_date = self.request.query_params.get("date_from", None)
        end_date = self.request.query_params.get("date_to", None)

        if not source_curr:
            return Response(
                {"error": True, "msg": "source currency required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not start_date:
            return Response(
                {"error": True, "msg": "date_from required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not end_date:
            return Response(
                {"error": True, "msg": "date_to required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            converted_start_date = datetime.datetime.strptime(
                start_date, "%Y-%m-%d"
            ).date()
            converted_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception as e:
            return Response(
                {
                    "error": True,
                    "msg": "invalid date_from or date_to format",
                    "data": "",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if the source currency is a valid currency or not
        curr_obj = (
            Currency.objects.filter(code=source_curr, is_deleted=False).values().first()
        )

        if not curr_obj:
            return Response(
                {"error": True, "msg": "invalid source currency", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        currencies_objs_lst = Currency.objects.filter(is_deleted=False).values(
            "id", "code"
        )
        currencies_objs = {obj["code"]: obj["id"] for obj in currencies_objs_lst}

        data_lst = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_curr,
            valuation_date__gte=start_date,
            valuation_date__lte=end_date,
            is_deleted=False,
        ).values(
            "source_currency",
            "exchanged_currency",
            "valuation_date",
            "rate_value",
        )

        if data_lst:
            data_obj = format_db_data(data_lst)
        else:
            data_obj = {}

        if len(data_obj.keys()) != (converted_end_date - converted_start_date).days + 1:
            data_lst = get_exchange_rate_data(
                source_curr=source_curr,
                valuation_date=str(datetime.datetime.now().date()),
                provider_name="CurrencyBeacon",
                operations="timeseries",
                exchange_curr=None,
                start_date=start_date,
                end_date=end_date,
            )

            if data_lst["error"]:
                return Response(data_lst)

            bulk_create_lst = []

            for keys in data_lst["data"].keys():
                if keys not in data_obj:
                    for inner_keys in data_lst["data"][keys]:
                        bulk_create_lst.append(
                            CurrencyExchangeRate(
                                source_currency_id=currencies_objs[source_curr],
                                exchanged_currency_id=currencies_objs[inner_keys],
                                valuation_date=keys,
                                rate_value=data_lst["data"][keys][inner_keys],
                            )
                        )

            CurrencyExchangeRate.objects.bulk_create(bulk_create_lst)
            return Response(data_lst["data"])

        return Response(data_obj)


class ConvertCurrencyApi(views.APIView):
    """
    This class is used to get the object of a converted currency.

    Args:-
        source_currency - Base currency code
        exchanged_currency - Exchange currency code
        amount - valid positive integer
    """

    def get(self, request, *args, **kwargs):
        source_curr = self.request.query_params.get("source_currency", None)
        exchanged_curr = self.request.query_params.get("exchanged_currency", None)
        amount = self.request.query_params.get("amount", None)

        if not source_curr:
            return Response(
                {"error": True, "msg": "source currency required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not exchanged_curr:
            return Response(
                {"error": True, "msg": "exchanged currency required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not amount:
            return Response(
                {"error": True, "msg": "amount required", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = int(amount)
        except Exception as e:
            return Response(
                {"error": True, "msg": "amount should be integer type", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amount <= 0:
            return Response(
                {"error": True, "msg": "invalid amount", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if the source currency is a valid currency or not
        source_curr_obj = (
            Currency.objects.filter(code=source_curr, is_deleted=False).values().first()
        )

        if not source_curr_obj:
            return Response(
                {"error": True, "msg": "invalid source currency", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        exchanged_curr_obj = (
            Currency.objects.filter(code=exchanged_curr, is_deleted=False)
            .values()
            .first()
        )

        if not exchanged_curr_obj:
            return Response(
                {"error": True, "msg": "invalid exchanged currency", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # checking in db for the provided details
        curr_exc_rate_value = (
            CurrencyExchangeRate.objects.filter(
                source_currency_id=source_curr_obj["id"],
                exchanged_currency_id=exchanged_curr_obj["id"],
                valuation_date=str(datetime.datetime.now().date()),
                is_deleted=False,
            )
            .values_list("rate_value", flat=True)
            .first()
        )

        if not curr_exc_rate_value:
            data_obj = get_exchange_rate_data(
                source_curr=source_curr_obj["code"],
                valuation_date=str(datetime.datetime.now().date()),
                provider_name="CurrencyBeacon",
                operations="converter",
                exchange_curr=exchanged_curr_obj["code"],
                start_date=None,
                end_date=None,
                amount=1,
            )

            if data_obj["error"]:
                return Response(data_obj, status=status.HTTP_400_BAD_REQUEST)

            curr_exc_rate_value = data_obj["data"]["value"]
            CurrencyExchangeRate.objects.create(
                source_currency_id=source_curr_obj["id"],
                exchanged_currency_id=exchanged_curr_obj["id"],
                valuation_date=str(datetime.datetime.now().date()),
                rate_value=curr_exc_rate_value,
            )

        result = {
            "sorce_currency": source_curr_obj["code"],
            "exchanged_currency": exchanged_curr_obj["code"],
            "rate_value": curr_exc_rate_value,
            "total_amount": curr_exc_rate_value * amount,
        }

        return Response(result, status=status.HTTP_200_OK)


class CurrencyModelView(ModelViewSet):
    """This class is used for all the CRUD operations for Currency"""

    queryset = Currency.objects.filter(is_deleted=False)
    serializer_class = CurrencySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
