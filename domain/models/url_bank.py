from django.db import models
from domain.models.base_model import BaseModel


class UrlBank(BaseModel):
    actual_url = models.CharField(max_length=3000)
    actual_url_shortened = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'url_bank'
        app_label = 'domain'
