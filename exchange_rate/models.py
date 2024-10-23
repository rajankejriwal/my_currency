from django.db import models
from my_currency.base_model import BaseModel


class Currency(BaseModel):
    """Class to store the details about the currency."""

    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class CurrencyExchangeRate(BaseModel):
    """Class to store the details about the exchange details."""

    source_currency = models.ForeignKey(
        "Currency", related_name="source_crr_exc", on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(
        "Currency", related_name="exchanged_crr_exc", on_delete=models.CASCADE
    )
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
