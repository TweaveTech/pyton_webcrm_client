"""
# A copy/paste for debugging / testing

from src.webcrm.api import WebCrmAPI
import os
API_TOKEN = os.environ['WebCrmApiKey']

api = WebCrmAPI(api_token=API_TOKEN)
# next(api.organisations())
api.organisation_by_id(2)

"""
import os
import unittest
from pathlib import Path
import datetime

from src.webcrm.api import WebCrmAPI

API_TOKEN = os.environ['WebCrmApiKey']


class WebCrmClientMixin:
    def setUp(self):
        super().setUp()
        self.api = WebCrmAPI(api_token=API_TOKEN, verbose=True)


class OrganisationsCase(WebCrmClientMixin, unittest.TestCase):
    def test_organisations(self):
        organisation = next(self.api.organisations())
        self.assertTrue(isinstance(organisation, tuple))

    def test_organisation_by_id(self):
        organisation_id = next(self.api.organisations()).organisation_id
        organisation = self.api.organisation_by_id(organisation_id)
        self.assertEqual(organisation_id, organisation.organisation_id)

    def test_persons(self):
        person = next(self.api.persons())
        self.assertTrue(isinstance(person, tuple))

    def test_person_by_id(self):
        person_id = next(self.api.persons()).person_id
        person = self.api.person_by_id(person_id)
        self.assertEqual(person_id, person.person_id)