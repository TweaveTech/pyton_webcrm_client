from functools import wraps
from time import sleep

import logging
logger = logging.getLogger(__name__)


def auto_token():
    '''
    Automatically request a fresh token should access 
    be denied:
    https://webcrm.com/uk/support/api/rest-api/
    '''
    def deco_f(f):

        @wraps(f)
        def wrap_f(self, *args, **kwargs):
            resp = f(self, *args, **kwargs)

            if resp.status_code in [401]:
                self._set_jwt_token()
                resp = f(self, *args, **kwargs)

            return resp

        return wrap_f

    return deco_f


def retry_rate_limit():
    '''
    Retry when the request has run into rate limiting.
    https://api.webcrm.com/documentation/index.html
    '''
    def deco_f(f):

        @wraps(f)
        def wrap_f(self, *args, **kwargs):
            retry_after = 1

            while retry_after > 0:
                resp = f(self, *args, **kwargs)
                
                if resp.status_code in [429]:
                    json = resp.json()
                    retry_after = json['RetryAfterSeconds']
                    sleep(retry_after)
                else:
                    return resp

        return wrap_f

    return deco_f
