from __future__ import absolute_import
import datetime
from .. import models
import factory
from django.core.mail.message import EmailMultiAlternatives


def make_message(subject="Example subject",
                 from_addr="from@example.com",
                 to_addr="to@example.com",
                 text="Lorem ipsum",
                 html_text=None):
    mail = EmailMultiAlternatives(subject, text, from_addr, [to_addr])
    if html_text:
        mail.attach_alternative(html_text, 'text/html')
    return mail


class EmailField(factory.django.FileField):
    DEFAULT_FILENAME = 'example.eml'

    def _make_data(self, params):
        """Create data for the field."""
        return make_message(subject=params.get('subject', "Example subject"),
                            from_addr=params.get("from_addr", "from@example.com"),
                            to_addr=params.get("to_addr", "to@example.com"),
                            text=params.get("text", "Lorem ipsum")).as_string()


class LetterFactory(factory.django.DjangoModelFactory):
    case = factory.SubFactory('foundation.cases.tests.factories.CaseFactory')
    subject = factory.Sequence('letter-subject-/{0}/'.format)
    content = factory.Sequence('letter-text-/{0}/ {{EMAIL}}'.format)

    class Meta:
        model = models.Letter


class IncomingLetterFactory(LetterFactory):
    sender = factory.LazyAttribute(lambda o: o.case.office)
    email = factory.Sequence('office-/{0}/@example.com'.format)

    class Meta:
        model = models.IncomingLetter
    # eml = EmailField(from_addr=factory.SelfAttribute('from_email'),
    #                  to_addr=factory.SelfAttribute('case.receiving_email'),
    #                  subject=factory.SelfAttribute('subject'),
    #                  text=factory.SelfAttribute('content'))


class OutgoingLetterFactory(LetterFactory):
    author = factory.SubFactory('foundation.users.tests.factories.UserFactory')
    email = factory.SubFactory('foundation.offices.tests.factories.EmailFactory')

    class Meta:
        model = models.OutgoingLetter


class SendOutgoingLetterFactory(LetterFactory):
    sender = factory.LazyAttribute(lambda o: o.case.created_by)
    send_at = factory.LazyAttribute(lambda o: datetime.datetime.utcnow() +
                                    datetime.timedelta(hours=1))
    # eml = EmailField(from_addr=factory.SelfAttribute('send_at'),
    #                  to_addr=factory.SelfAttribute('email.email'),
    #                  subject=factory.SelfAttribute('subject'),
    #                  text=factory.SelfAttribute('content'))
