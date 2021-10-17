import logging
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.conf import settings

from url_shortener_app.services.utility_service import live_url_check, string_to_md5_hash, create_short_url
from domain.models.url_bank import UrlBank, get_default_expiration_date

HOMEPAGE_TEMPLATE = 'home/index.html'
logger = logging.getLogger(__name__)


class HomePage(View):
    def get(self, request):
        return render(request, HOMEPAGE_TEMPLATE, {})

    def post(self, request):
        try:
            main_url = request.POST.get('main_url', None)
            if main_url and live_url_check(main_url):
                md5_hash = string_to_md5_hash(main_url)
                url_bank_queryset = UrlBank.objects.filter(md_five_hash=md5_hash).exists()
                domain_name = settings.SITE_DOMAIN_NAME
                if url_bank_queryset:
                    actual_url_shortened = UrlBank.objects.filter(
                        md_five_hash=md5_hash).values_list('actual_url_shortened', flat=True).first()
                    shorten_url = actual_url_shortened
                    one_year_expiration_date = get_default_expiration_date()
                    UrlBank.objects.filter(md_five_hash=md5_hash).update(
                        expiration_date=one_year_expiration_date)
                else:
                    shorten_url = create_short_url(main_url, md5_hash)
                return render(request, HOMEPAGE_TEMPLATE, {'shorten_url': domain_name+shorten_url, 'status': 'success'})
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return render(request, HOMEPAGE_TEMPLATE, {'message': 'Invalid URL', 'status': 'error'})


class URLDecode(View):

    def get(self, request, short_url):
        try:
            url_bank_queryset = UrlBank.objects.filter(actual_url_shortened=short_url,
                                                       expiration_date__gte=datetime.now()).exists()
            if url_bank_queryset:
                actual_url_queryset = UrlBank.objects.filter(
                    actual_url_shortened=short_url).values_list('actual_url', flat=True).first()
                url_path = actual_url_queryset
                return HttpResponseRedirect(url_path)
            else:
                expired_url_queryset = UrlBank.objects.filter(actual_url_shortened=short_url,
                                                              expiration_date__lt=datetime.now()).exists()
                if expired_url_queryset:
                    UrlBank.objects.filter(actual_url_shortened=short_url).delete()
                return render(request, {'message': 'URL not found!'})
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return render(request, HOMEPAGE_TEMPLATE, {})
