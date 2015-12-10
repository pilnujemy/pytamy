from __future__ import unicode_literals
import uuid
import claw
import os
from atom.models import AttachmentBase
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.files import File
from django.dispatch import receiver
from django.conf import settings
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField
from django.core.files.base import ContentFile
from foundation.cases.models import Case
from django_bleach.models import BleachField
from foundation.offices.models import Office
from django_mailbox.signals import message_received
from django.db.models.signals import pre_save
from django.utils import timezone
from django_mailbox.models import Message
from .email import MessageTemplateEmail
from .utils import nl2br

INCOMING_HELP = _("Is it a incoming message? Otherwise, it is outgoing.")

claw.init()


class LetterQuerySet(models.QuerySet):
    def with_attachment_count(self):
        return self.annotate(attachment_count=models.Count('attachment'))

    def for_milestone(self):
        return (self.select_related('case').
                for_list().
                with_attachment_count())

    def _for_item(self):
        return self.select_related('author', 'sender_user', 'sender_office',
                                   'case__created_by', 'case__office')

    def for_list(self):
        return self.with_attachment_count()._for_item()

    def for_detail(self):
        return self._for_item().prefetch_related('attachment_set')


class Letter(TimeStampedModel):
    # General
    case = models.ForeignKey('cases.Case')
    subject = models.CharField(verbose_name=_("Subject"), max_length=50)
    slug = AutoSlugField(populate_from='subject', verbose_name=_("Slug"), unique=True)
    content = BleachField(strip_tags=True)
    quote = BleachField(strip_tags=True)
    incoming = models.BooleanField(default=False, verbose_name=_("Incoming"),
                                   help_text=INCOMING_HELP)
    eml = models.FileField(upload_to="eml_msg/%Y/%m/%d/", null=True, blank=True)
    msg = models.ForeignKey(to=Message,
                            null=True,
                            blank=True,
                            help_text=_("Message registered by django_mailbox"))
    # Outgoing
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    send_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="author_letter",
                               null=True,
                               blank=True)
    email = models.ForeignKey('offices.Email', null=True, blank=True)
    # Incoming
    sender_office = models.ForeignKey(Office, null=True, blank=True, related_name='sender_office')
    from_email = models.CharField(verbose_name=_("From e-mail"),
                                  max_length=100,
                                  null=True,
                                  help_text=_("Field valid only for incoming messages"))
    objects = LetterQuerySet.as_manager()

    def recipient(self):
        return self.email.office

    @property
    def sender(self):
        return self.sender_user or self.sender_office

    @sender.setter
    def sender(self, value):
        if isinstance(value, Office):
            self.sender_office = value
            self.sender_user = None
        else:
            self.sender_user = value
            self.sender_office = None

    def is_send(self):
        return bool(self.eml)

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")
        ordering = ['created', ]

    def __unicode__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('letters:details', kwargs={'slug': self.slug})

    def send(self, user):
        text = self.content.replace('{{EMAIL}}', self.case.receiving_email)
        to = self.email.email
        # Construct MimeText instance
        context = dict(text=text,
                       office=self.email.office,
                       case=self.case,
                       letter=self,
                       email=self.case.receiving_email,
                       subject=self.subject)
        msg = MessageTemplateEmail().make_email_object(to=to,
                                                       context=context)
        msg.extra_headers.update({'Return-Receipt-To': self.case.receiving_email,
                                  'Disposition-Notification-To': self.case.receiving_email})
        msg.from_email = self.case.receiving_email
        # Save MimeText to file
        self.eml.save('%s.eml' % uuid.uuid4(),
                      ContentFile(msg.message().as_string()),
                      save=False)
        # Update instance
        self.sender_user = user
        self.incoming = False
        # Save instance
        self.save()
        # Send message
        msg.send()
        return msg

    @classmethod
    def process_incoming(cls, case, message):
        if message.html:
            text = claw.quotations.extract_from(message.html, 'text/html')
            quote = message.text.replace(text, '')
        else:
            text = nl2br(claw.quotations.extract_from(message.text, 'text/plain'))
            quote = nl2br(message.text.replace(text, ''))
        obj = cls.objects.create(sender_office=case.office,
                                 from_email=message.from_address[0],
                                 case=case,
                                 subject=message.subject,
                                 content=text,
                                 quote=quote,
                                 incoming=True,
                                 msg=message,
                                 eml=File(message.eml, message.eml.name))
        attachments = []
        # Append attachments
        for attachment in message.attachments.all():
            name = attachment.get_filename() or 'Unknown.bin'
            name = name.encode('ascii', 'ignore')
            if len(name) > 70:
                name, ext = os.path.splitext(name)
                ext = ext[:70]
                name = name[:70 - len(ext)] + ext
            file_obj = File(attachment.document, name)
            att_obj = Attachment(letter=obj, attachment=file_obj)
            attachments.append(att_obj)
        Attachment.objects.bulk_create(attachments)
        return obj, attachments


class Attachment(AttachmentBase):
    letter = models.ForeignKey(Letter)


@receiver(message_received)
def mail_process(sender, message, **args):
    try:
        case = Case.objects.get(receiving_email=message.to_addresses[0])
    except Case.DoesNotExist:
        print("Message #{pk} skip, due not recognized address {to}".
              format(pk=message.pk, to=message.to_addresses[0]))
        return
    letter, attachments = Letter.process_incoming(case, message)
    print("Message #{message} registered in case #{case} as letter #{letter}".
          format(message=message.pk, case=case.pk, letter=letter.pk))


@receiver(pre_save, sender=Letter)
def update_send_at(sender, instance, **kwargs):
    if (not instance.incoming and  # outgoing
            not instance.send_at and  # no send time
            instance.eml):  # send msg set up
        instance.send_at = timezone.now()
