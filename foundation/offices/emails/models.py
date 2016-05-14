from __future__ import unicode_literals


from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Email(TimeStampedModel):
    office = models.ForeignKey('offices.Office', verbose_name=_("Office"))
    email = models.EmailField(verbose_name=_("Address"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="office_email")
    valid = models.BooleanField(default=True,
                                verbose_name=_("Is valid?"),
                                help_text=_("Identify if email is valid (still)."))

    class Meta:
        verbose_name = _("E-mail address")
        verbose_name_plural = _("E-mail addresses")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "%s?email=%d" % (reverse('cases:create'), self.pk)
