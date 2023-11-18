import os
from twocaptcha import TwoCaptcha

API_KEY = os.environ.get("API_KEY")


def solve_recaptcha(site_key, url):
    api_key = os.getenv('APIKEY_2CAPTCHA', API_KEY)

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=site_key,
            url=url)

    except Exception as e:
        print(e)

    else:
        return result
