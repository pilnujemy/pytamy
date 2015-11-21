from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField
from django.db.models.signals import post_save


class CaseQuerySet(models.QuerySet):
    pass


class Case(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    office = models.ForeignKey('offices.Office')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = PassThroughManager.for_queryset_class(CaseQuerySet)()
    receiving_email = models.CharField(max_length=150,
                                       verbose_name=_("Receiving email"),
                                       help_text=_("Address used to receiving emails."))

    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")
        ordering = ['created', ]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cases:details', kwargs={'slug': self.slug})


def update_receiving_email(sender, instance, **kwargs):
    if not instance.receiving_email:
        instance.receiving_email = settings.MAILBOX_RECEIVING_PROTOTYPE.format(**instance.__dict__)
        instance.save()

post_save.connect(update_receiving_email, sender=Case, dispatch_uid="update_receiving_email")
