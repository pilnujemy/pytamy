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
from ..models import Letter
from django_mailbox.models import Mailbox


class TestLetter(TestCase):
    def setUp(self):
        self.object = OutgoingLetterFactory(subject="Example subj")
        self.mailbox = Mailbox(name="My mailbox")
        self.mailbox.save()
        super(TestLetter, self).setUp()

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
        self.object.send(user)

        # Send message
        msg = mail.outbox[0]
        text = msg.message().as_string().decode('utf-8')
        self.assertIn('From: %s' % (self.object.case.receiving_email), text)
        self.assertIn('Subject: %s' % (self.object.subject), text)
        self.assertIn(self.object.content, text)

        # Save data
        self.assertTrue(self.object.eml)
        self.assertEqual(self.object.sender_user, user)
        self.assertTrue(self.object.send_at)
        self.assertEqual(self.object.incoming, False)

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
        letter, attachments = Letter.process_incoming(case, msg)
        self.assertEqual(letter.attachment_set.all().count(), 1)
