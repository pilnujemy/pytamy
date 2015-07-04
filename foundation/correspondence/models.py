import os
import datetime
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    street = models.CharField(max_length=250, null=True, blank=True, verbose_name=_('Street'))
    city = models.CharField(max_length=250, null=True, blank=True, verbose_name=_("City"))
    postcode = models.CharField(max_length=6, verbose_name=_("Post-code"))
    comment = models.TextField(verbose_name=_("Comment"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contact_created",
        verbose_name=_("Created by"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("Created on"))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Modified by"),
                                    null=True, related_name="contact_modified",)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True,
        verbose_name=_("Modified on"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('correspondence:contact_detail', kwargs={'pk': str(self.pk)})


class Letter(models.Model):
    outgoing = models.BooleanField(default=True, verbose_name=_("Outgoing"))
    contact = models.ForeignKey(to=Contact, verbose_name=_("Contact"))
    transfer_on = models.DateField(verbose_name=_("Transfer on"), default=datetime.date.today,
        help_text=_("Receive date for incoming, send date for outgoing"))
    description = models.CharField(max_length=250, verbose_name=_("Description"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="letter_created",
        verbose_name=_("Created by"))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_("Created on"))
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Modified by"),
                                    null=True, related_name="letter_modified",)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True,
        verbose_name=_("Modified on"))

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")

    def __unicode__(self):
        return _("Letter #%s") % (str(self.pk))

    def get_absolute_url(self):
        return reverse('correspondence:letter_detail', kwargs={'pk': str(self.pk)})


class Attachment(models.Model):
    letter = models.ForeignKey(Letter, verbose_name=_("Letter"))
    file = models.FileField(verbose_name=("File"), upload_to="correspondence_attachment")

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __unicode__(self):
        return self.filename()
