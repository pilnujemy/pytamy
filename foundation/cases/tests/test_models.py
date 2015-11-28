from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import CaseFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings
from ..models import Case


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

    @override_settings(MAILBOX_RECEIVING_PROTOTYPE='example-{id}@example.com')
    def test_receiving_email(self):
        self.assertEqual(CaseFactory(pk=75).receiving_email, 'example-75@example.com')


class TestCaseQuerySet(TestCase):
    @override_settings(MAILBOX_RECEIVING_PROTOTYPE='example-{id}@example.com')
    def test_by_rcv_email(self):
        CaseFactory(pk=75)
        self.assertEqual(Case.objects.by_rcv_email('example-75@example.com').get().pk, 75)
