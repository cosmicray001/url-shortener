from datetime import datetime, timedelta

from django.db import models
from domain.models.base_model import BaseModel


def get_default_expiration_date():
    return datetime.now() + timedelta(days=365)


class UrlBank(BaseModel):
    actual_url = models.CharField(max_length=3000)
    expiration_date = models.DateTimeField(default=get_default_expiration_date)
    md_five_hash = models.CharField(max_length=32, db_index=True)
    actual_url_shortened = models.CharField(max_length=10, db_index=True)

    class Meta:
        db_table = 'url_bank'
        app_label = 'domain'
