from django.contrib import admin
from domain.models.url_bank import UrlBank


@admin.register(UrlBank)
class FailedLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'actual_url', 'md_five_hash', 'actual_url_shortened', 'expiration_date', )
