from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField
from django_bleach.models import BleachField
from foundation.offices.models import Office


class LetterQuerySet(models.QuerySet):
    pass


class Letter(TimeStampedModel):
    case = models.ForeignKey('cases.Case')
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    content = BleachField()
    email = models.ForeignKey('offices.Email', null=True, blank=True)
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    sender_office = models.ForeignKey(Office, null=True, blank=True, related_name='sender_office')
    objects = PassThroughManager.for_queryset_class(LetterQuerySet)()

    @property
    def author(self):
        return self.sender_user or self.sender_office

    @author.setter
    def author(self, value):
        if isinstance(value, Office):
            self.sender_office = value
            self.sender_user = None
        else:
            self.sender_user = value
            self.sender_office = None

    @property
    def is_outgoing(self):
        return not self.email

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")
        ordering = ['created', ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('letters:details', kwargs={'slug': self.slug})

    def send_to_office(self, user):
        from foundation.mail_messages.models import Message
        return Message.create_for_letter(letter=self, user=user)
