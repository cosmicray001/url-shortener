from django.shortcuts import render
from django.views import View
from django.conf import settings

from url_shortener_app.services.utility_service import live_url_check, string_to_md5_hash, create_short_url
from domain.models.url_bank import UrlBank, get_default_expiration_date


class HomePage(View):
    def get(self, request):
        return render(request, 'home/index.html', {})

    def post(self, request):
        try:
            main_url = request.POST.get('main_url', None)
            if main_url and live_url_check(main_url):
                md5_hash = string_to_md5_hash(main_url)
                url_bank_queryset = UrlBank.objects.filter(md_five_hash=md5_hash).first()
                domain_name = settings.SITE_DOMAIN_NAME
                if url_bank_queryset:
                    shorten_url = url_bank_queryset.actual_url_shortened
                    one_year_expiration_date = get_default_expiration_date()
                    expiration_date_update = UrlBank.objects.filter(md_five_hash=md5_hash).update(
                        expiration_date=one_year_expiration_date)
                else:
                    shorten_url = create_short_url(main_url, md5_hash)
                return render(request, 'home/index.html', {'shorten_url': domain_name+shorten_url})
        except Exception as ex:
            print(ex)
        return render(request, 'home/index.html', {'message': 'Invalid URL'})
