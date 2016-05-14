from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import OfficeFactory
from ..models import Office
from foundation.users.tests.factories import UserFactory
from foundation.teryt.tests.factories import JSTFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import activate


def assign_perm(user, model, codename):
    content_type = ContentType.objects.get_for_model(model)
    permission = Permission.objects.get(content_type=content_type, codename=codename)
    user.user_permissions.add(permission)


class TestOffice(TestCase):
    def setUp(self):
        self.object = OfficeFactory(name="testname")

    def test__str__(self):
        activate('en')
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

        self.assertEqual(
            OfficeFactory(name="testname", visible=False).__str__(),
            "testname (hidden)"
        )
        self.assertEqual(
            OfficeFactory(name="testname", visible=True).__str__(),
            "testname"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/urzedy/testname'
        )


class TestOfficeQuerySet(TestCase):
    def setUp(self):
        self.object = OfficeFactory()

    def test_for_user_can_change(self):
        user = UserFactory()
        assign_perm(user, Office, 'delete_office')
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(visible=True).pk).exists())
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(visible=False).pk).exists())

    def test_for_user_can_not_change(self):
        user = UserFactory()
        self.assertTrue(Office.objects.for_user(user).
                        filter(pk=OfficeFactory(visible=True).pk).exists())
        self.assertFalse(Office.objects.for_user(user).
                         filter(pk=OfficeFactory(visible=False).pk).exists())

    def _area_tester(self, stack, nedle, result):
        self.assertEqual(Office.objects.area(stack).
                         filter(pk=OfficeFactory(jst=nedle).pk).exists(), result)

    def test_area_self(self):
        a = JSTFactory()
        self._area_tester(a, a, True)

    def test_area_contains(self):
        a = JSTFactory()
        a_child = JSTFactory(parent=a)
        self._area_tester(a, a_child, True)
        self._area_tester(a_child, a, False)

    def test_area_indepenent(self):
        a = JSTFactory()
        b = JSTFactory()
        self._area_tester(b, a, False)
        self._area_tester(a, b, False)
