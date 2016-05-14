from test_plus.test import TestCase

from ..models import Email
from .factories import EmailFactory
from foundation.offices.tests.factories import OfficeFactory


class EmailTest(TestCase):
    def setUp(self):
        self.obj = EmailFactory(email="smith@example.com")

    def test__str__(self):
        self.assertEqual(self.obj.__str__(), "smith@example.com")
