from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import OfficeFactory


class TestUser(TestCase):
    def setUp(self):
        self.object = OfficeFactory(name="testname")

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

        self.assertEqual(
            OfficeFactory(name="testname", state='destroyed').__str__(),
            "testname (destroyed)"
        )
        self.assertEqual(
            OfficeFactory(name="testname", verified=False).__str__(),
            "testname (unverified)"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/urzedy/urzad-testname'
        )
