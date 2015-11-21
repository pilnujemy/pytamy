import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.base import ContentFile
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField
from foundation.letters.models import Letter
from .email import MessageTemplateEmail

INCOMING_HELP = _("Is it a incoming message? Otherwise, it is outgoing.")


class MessageQuerySet(models.QuerySet):
    pass


class Message(TimeStampedModel):
    letter = models.ForeignKey(Letter, verbose_name=("Letter"))
    subject = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='subject', verbose_name=_("Slug"))
    email = models.EmailField(max_length=250)
    incoming = models.BooleanField(default=False, verbose_name=_("Incoming"),
                                   help_text=INCOMING_HELP)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    eml = models.FileField(upload_to="eml_msg/%Y/%m/%d/")
    objects = PassThroughManager.for_queryset_class(MessageQuerySet)()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['created', ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mail_messages:details', kwargs={'slug': self.slug})

    @classmethod
    def create_for_letter(cls, user, letter):
        if not letter.email:
            raise Exception("Unable to send letter with no email")
        # Create empty Message
        obj = cls()
        # Generate text

        text = letter.content.replace('{{EMAIL}}', letter.case.receiving_email)
        to = letter.email.email
        # Construct MimeText instance
        context = dict(text=text,
                       office=letter.email.office,
                       case=letter.case,
                       letter=letter,
                       email=letter.case.receiving_email)
        msg = MessageTemplateEmail().make_email_object(to=to,
                                                       context=context)
        msg.extra_headers.update({'Return-Receipt-To': letter.case.receiving_email,
                           'Disposition-Notification-To': letter.case.receiving_email})
        msg.from_email = letter.case.receiving_email
        # Save MimeText to file
        obj.eml.save('%s.eml' % uuid.uuid4(),
                     ContentFile(msg.message().as_string()),
                     save=False)

        # Assign attribute of Message
        obj.letter = letter
        obj.subject = msg.subject[:50]
        obj.to = to
        obj.incoming = False
        obj.user = user
        obj.save()
        msg.send()
        return obj
