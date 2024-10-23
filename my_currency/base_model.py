from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.DO_NOTHING
    )

    class Meta:
        abstract = True
