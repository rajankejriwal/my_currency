from django.contrib import admin
from adapters.models import *


class ProviderAdmin(admin.ModelAdmin):

    readonly_fields = ("id", "deleted_at", "deleted_by")
    list_display = (
        "id",
        "name",
        "is_active",
        "priority",
        "meta_data",
        "deleted_at",
        "is_deleted",
        "deleted_by",
    )

    model_name = "Provider Record(s)"


admin.site.register(Provider, ProviderAdmin)
