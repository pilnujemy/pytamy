from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import OfficeFactory, EmailFactory
from ..models import Office, Email
from foundation.users.tests.factories import UserFactory
from foundation.teryt.tests.factories import JSTFactory
from ..forms import OfficeForm


class OfficeFormTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_init(self):
        OfficeForm(user=UserFactory())

    def test_init_without_user(self):
        with self.assertRaises(ValueError):
            OfficeForm()

    def test_valid_data(self):
        jst = JSTFactory()
        parent = OfficeFactory()
        form = OfficeForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'jst': jst.pk,
            'parent': [parent.pk],
            'tags': 'ministerstwo',
        }, user=self.user)
        form.is_valid()
        self.assertTrue(form.is_valid())
        obj = form.save()
        self.assertEqual(obj.name, "Turanga Leela")
        self.assertEqual(obj.jst.pk, str(jst.pk))
        self.assertEqual(parent in list(obj.parent.all()), True)
        self.assertEqual(obj.created_by, self.user)
        # self.assertEqual(Email.objects.filter(office=obj).get().email, "leela@example.com")

        # email = form.save_email()
        # self.assertEqual(Email.objects.filter(office=obj).count(), 1)
        # self.assertEqual(email.office, obj)
        # self.assertEqual(email.created_by, obj.created_by)
        # self.assertEqual(email.email, "leela@example.com")
