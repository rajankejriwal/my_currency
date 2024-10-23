from django.urls import path, include
from rest_framework.routers import DefaultRouter

from exchange_rate import views


router = DefaultRouter()
router.register(r"", views.CurrencyModelView, basename="currency")


urlpatterns = [
    path(
        "currency-time-series/",
        views.CurrencyListApi.as_view(),
        name="currency-time-series",
    ),
    path(
        "convert-currency/",
        views.ConvertCurrencyApi.as_view(),
        name="convert-currency",
    ),
    path("currency/", include(router.urls)),
]
