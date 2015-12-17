from __future__ import absolute_import, unicode_literals
import os
import email
import six

from test_plus.test import TestCase
from foundation.users.tests.factories import UserFactory
from foundation.cases.tests.factories import CaseFactory
from django.core import mail
from .factories import (SendOutgoingLetterFactory, make_message, OutgoingLetterFactory,
                        IncomingLetterFactory)
from ..models import Letter, IncomingLetter, OutgoingLetter
from django_mailbox.models import Mailbox


class LetterQuerySetTestCase(TestCase):
    def test_valid_with_attachment_count(self):
        Letter.objects.with_attachment_count().all().first()

    def test_valid_for_milestone(self):
        Letter.objects.for_milestone().all().first()

    def test_valid_for_item(self):
        Letter.objects.filter()._for_item().all().first()

    def test_valid_for_list(self):
        Letter.objects.for_list().all().first()

    def test_valid_for_detail(self):
        Letter.objects.for_detail().all().first()

    def _exists(self, call, result=True):
        qs = Letter.objects
        self.assertEqual(call(qs).exists(), result)

    def test_outgoing(self):
        self._exists(lambda x: x.outgoing().filter(pk=IncomingLetterFactory().pk), False)
        self._exists(lambda x: x.outgoing().filter(pk=OutgoingLetterFactory().pk), True)

    def test_incoming(self):
        self._exists(lambda x: x.incoming().filter(pk=IncomingLetterFactory().pk), True)
        self._exists(lambda x: x.incoming().filter(pk=OutgoingLetterFactory().pk), False)


class TestOutgoingLetterFactory(TestCase):
    def setUp(self):
        self.object = OutgoingLetterFactory(subject="Example subj")
        super(TestOutgoingLetterFactory, self).setUp()

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "Example subj"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/listy/list-example-subj'
        )

    def test_send(self):
        user = UserFactory()
        self.assertFalse(self.object.eml)
        self.assertFalse(self.object.is_send())
        self.object.send(user)

        # Send message
        msg = mail.outbox[0]
        text = msg.message().as_string().decode('utf-8')
        self.assertIn('From: %s' % (self.object.case.receiving_email), text)
        self.assertIn('Subject: %s' % (self.object.subject), text)
        self.assertIn(self.object.content, text)

        # Save data
        self.assertTrue(self.object.eml)
        self.assertEqual(self.object.sender, user)
        self.assertTrue(self.object.send_at)
        self.assertTrue(self.object.is_send(), True)


class TestIncomingLetter(TestCase):
    def setUp(self):
        self.mailbox = Mailbox.objects.create(name="My mailbox")
        super(TestIncomingLetter, self).setUp()

    def _get_email_as_text(self, name):
        with open(
            os.path.join(
                os.path.dirname(__file__),
                'messages',
                name,
            ),
            'rb'
        ) as f:
            return f.read()

    def _get_email_object(self, name):
        copy = self._get_email_as_text(name)
        if six.PY3:
            msg = email.message_from_bytes(copy)
        else:
            msg = email.message_from_string(copy)
        return self.mailbox._process_message(msg)

    def test_process_incoming_unicode_attachment(self):
        case = CaseFactory(receiving_email='sprawa-8@badanie.pilnujemy.info')
        msg = self._get_email_object('unicode-filename-attachment-reply.eml')
        letter, attachments = IncomingLetter.process_incoming(case, msg)
        self.assertEqual(letter.attachment_set.all().count(), 1)

