from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import OfficeFactory
from ..models import Office
from foundation.users.tests.factories import UserFactory


class TestOffice(TestCase):
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


class TestOfficeQuerySet(TestCase):
    def setUp(self):
        self.object = OfficeFactory()

    def test_for_user_staff(self):
        user = UserFactory(is_staff=True)
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(state='accepted').pk).exists())
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(state='created').pk).exists())
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(state='accepted').pk).exists())

    def test_for_user_user(self):
        user = UserFactory(is_staff=False)
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(created_by=user, state='created').pk).exists())
        self.assertFalse(Office.objects.for_user(user).
                         filter(pk=OfficeFactory(state='created').pk).exists())
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(state='accepted').pk).exists())
