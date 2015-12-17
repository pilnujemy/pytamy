from test_plus.test import TestCase
from .factories import OutgoingLetterFactory
from foundation.users.tests.factories import UserFactory
from django.core.urlresolvers import reverse
from django.core import mail


class LetterSendViewTestCase(TestCase):
    def setUp(self):
        self.object = OutgoingLetterFactory(subject="Example")
        self.url = reverse('letters:send', kwargs={'slug': self.object.slug})
        super(LetterSendViewTestCase, self).setUp()

    def login(self):
        self.client.login(username=UserFactory(is_staff=True, is_superuser=True),
                          password='password')

    def test_reverse_url(self):
        self.assertEqual('/listy/list-example/~send', self.url)

    def test_display_subject(self):
        self.login()
        resp = self.client.get(self.url)
        self.assertContains(resp, self.object.subject)

    def test_send(self):
        self.login()
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
