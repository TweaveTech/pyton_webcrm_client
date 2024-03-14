import requests
from time import sleep

from .helpers import convert_dict_to_namedtuple
from .exceptions import EmptyPage, RequestError, JSONDecodeError
from .decorators import auto_token, retry_rate_limit, raise_empty_page

import logging
logger = logging.getLogger(__name__)


class WebCrmAPI:
    def __init__(self, api_token, verbose=False):
        self.headers = {}
        self.api_token = api_token
        self.base_url = "https://api.webcrm.com/"
        self.verbose = verbose

        self.base_names = convert_dict_to_namedtuple("BaseNames",{
            "organisations": "Organisations",
            "persons": "Persons",
            "memberships": "Memberships"
        })

    def _get_endpoint_url(self, endpoint):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        if self.verbose:
            logger.debug(url)
            print(url)

        return url

    def _set_jwt_token(self):
        endpoint = '/Auth/ApiLogin'
        data = {'authCode': self.api_token}
        resp = self._post(endpoint, data=data)
        token = resp.json()['AccessToken']
        self.headers['Authorization'] = f'Bearer {token}'

    @auto_token()
    @retry_rate_limit()
    @raise_empty_page()
    def _get(self, endpoint):
        url = self._get_endpoint_url(endpoint)
        resp = requests.get(url, headers=self.headers)
        return resp

    def _get_json(self, endpoint):
        resp = self._get(endpoint)

        if not resp.ok:
            status_code = resp.status_code
            raise RequestError(f"GET {endpoint=} returned {status_code=}")

        return resp.json()

    def _paged_get_json(self, endpoint, page=1, page_size=150):
        # We set the page to 0 in order to halt the loop
        # complete_resp = []

        while page > 0:
            paged_endpoint = f"{endpoint}?Page={page}&Size={page_size}"
            try:
                json = self._get_json(paged_endpoint)
                # complete_resp.extend(resp)
                yield json
                page += 1
            except EmptyPage:
                page = 0

        # return complete_resp

    @auto_token()
    @retry_rate_limit()
    def _post(self, endpoint, data):
        url = self._get_endpoint_url(endpoint)
        resp = requests.post(url, headers=self.headers, data=data)
        return resp

    def _generic_base_list(self, base_name):
        endpoint = f'/{base_name}'
        for page in self._paged_get_json(endpoint):
            for json in page:
                yield convert_dict_to_namedtuple(base_name, json)

    def _generic_base_by_id(self, base_name, base_id):
        endpoint = f'/{base_name}/{base_id}'
        return convert_dict_to_namedtuple(base_name, self._get_json(endpoint))

    def organisations(self):
        return self._generic_base_list(self.base_names.organisations)

    def organisation_by_id(self, organisations_id):
        return self._generic_base_by_id(self.base_names.organisations, organisations_id)

    def persons(self):
        return self._generic_base_list(self.base_names.persons)

    def person_by_id(self, persons_id):
        return self._generic_base_by_id(self.base_names.persons, persons_id)

    def person_by_organisation(self, organisations_id):
        base_name = self.base_names.persons
        endpoint = f"/{base_name}/ByOrganisation/{organisations_id}"
        for page in self._paged_get_json(endpoint):
            for person in page:
                yield convert_dict_to_namedtuple(base_name, person)
