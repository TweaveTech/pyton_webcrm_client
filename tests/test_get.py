import os
import unittest
from pathlib import Path
import datetime

from webcrm import WebCrmAPI

API_KEY = os.environ['WebCrmApiKey']


class WebCrmClientMixin:
    def setUp(self):
        super().setUp()
        self.api = WebCrmAPI(api_key=API_KEY)


class OrganisationsCase(WebCrmClientMixin, unittest.TestCase):
    def test_organisations(self):
        organisation = next(self.api.organisations())
        self.assertTrue(isinstance(organisation, tuple))

    def test_organisation_by_id(self):
        organisation_id = next(self.api.organisations()).organisation_id
        organisation = self.api.organisation_by_id(organisation_id)
        self.assertEqual(organisation_id, organisation.organisation_id)

    def test_persons(self):
        person = next(self.api.organisations())
        self.assertTrue(isinstance(organisation, tuple))

    def test_person_by_id(self):
        person_id = next(self.api.organisations()).person_id
        person = self.api.person_by_id(person_id).person_id
        self.assertEqual(person_id, person.person_id)

    def test_memberships(self):
        membership = next(self.api.memberships())
        self.assertTrue(isinstance(membership, tuple))

    def test_membership_by_id(self):
        membership_id = next(self.api.memberships()).membership_id
        membership = self.api.membership_by_id(membership_id)
        self.assertEqual(membership_id, membership.membership_id)