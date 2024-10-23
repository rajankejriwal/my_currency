from django.db import models
from my_currency.base_model import BaseModel
from jsonfield import JSONField


class Provider(BaseModel):
    """Class to store the provider details."""

    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(unique=True)
    meta_data = JSONField()
