from django.contrib import admin
from exchange_rate.models import *


class CurrencyAdmin(admin.ModelAdmin):

    readonly_fields = ("id", "deleted_at", "deleted_by")
    list_display = (
        "id",
        "code",
        "name",
        "symbol",
        "deleted_at",
        "is_deleted",
        "deleted_by",
    )

    model_name = "Currency Record(s)"


class CurrencyExchangeRateAdmin(admin.ModelAdmin):

    readonly_fields = ("id", "deleted_at", "deleted_by")
    list_display = (
        "id",
        "source_currency",
        "exchanged_currency",
        "valuation_date",
        "rate_value",
        "deleted_at",
        "is_deleted",
        "deleted_by",
    )

    model_name = "Currency Record(s)"


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
