from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import CaseFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def assign_perm(user, model, codename):
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(permission)


class TestCase(TestCase):
    def setUp(self):
        self.object = CaseFactory(name="testname")

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/sprawy/sprawa-testname'
        )

    def test_receiving_email(self):
        self.assertTrue(CaseFactory().receiving_email)


class TestCaseQuerySet(TestCase):
    pass
