import logging
import requests
import hashlib
from datetime import datetime

from django.conf import settings
from domain.models.url_bank import UrlBank
from url_shortener_app.services.encode import Encode

logger = logging.getLogger(__name__)


def live_url_check(url):
    """
    This function takes an URL and check whether it is live or not. If it is live return True and False otherwise.
    :param url: a Uniform Resource Locator(URL) of a website
    :return: True or False
    """
    try:
        r = requests.head(url)
        # print(r.status_code)
        return r.status_code == 200
    except Exception as E:
        logger.error(str(E), exc_info=True)
    return False


def string_to_md5_hash(string_to_hash):
    """
    This function takes a long string and converts it to md5 hash.
    :param string_to_hash: A long string
    :return: a 128bit md5 hash
    """
    result = hashlib.md5(string_to_hash.encode())
    # print(result.hexdigest())
    return result.hexdigest()


def create_short_url(main_url, original_md5_hash):
    """
    This function takes a main_url which is a long string and a md5_hash. Then it try to generate an unique short_url.
    After successfully creating unique short_url, it saves the info to the database.
    :param main_url: An actual url of a website(string)
    :param original_md5_hash: md5 hash(string)
    :return: create a shorten url and return it
    """
    encode = Encode()
    for short_url_try in range(settings.SHORT_URL_TRY):
        new_md5_hash = string_to_md5_hash(main_url+str(datetime.now()))
        short_url = encode.base62_encode(new_md5_hash)
        url_bank_queryset = UrlBank.objects.filter(actual_url_shortened=short_url).exists()
        if not url_bank_queryset:
            UrlBank.objects.create(
                actual_url=main_url, md_five_hash=original_md5_hash,
                actual_url_shortened=short_url)
            return short_url
    return None
