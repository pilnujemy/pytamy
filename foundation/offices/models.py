from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation.teryt.models import JST
from django.conf import settings
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from jsonfield import JSONField
from cached_property import cached_property
from pprint import pformat


REGON_HELP_TEXT = _("Compatible with National Official Register of National Economy Entities")


class OfficeQuerySet(QuerySet):
    def for_user(self, user):
        if user.has_perm('offices.delete_office'):
            return self
        return self.filter(visible=True)

    def area(self, jst):
        return self.filter(jst__tree_id=jst.tree_id,
                           jst__lft__gte=jst.lft,
                           jst__lft__lte=jst.rght)

    def for_list(self):
        return self


@python_2_unicode_compatible
class Office(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = models.ManyToManyField('self', blank=True)
    jst = models.ForeignKey(JST)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    visible = models.BooleanField(default=True,
                                  verbose_name=_("Verified"))
    postcode = models.CharField(max_length=6,
                                null=True,
                                blank=True,
                                verbose_name=_("Post code"))
    regon = models.CharField(max_length=10,
                             db_index=True,
                             null=True,
                             blank=True,
                             verbose_name=_("REGON"),
                             help_text=REGON_HELP_TEXT)
    krs = models.CharField(max_length=9,
                           db_index=True,
                           null=True,
                           blank=True,
                           verbose_name=_("Registration number"),
                           help_text=_("Compatible with Polish National Court Register"))
    extra = JSONField(default='{}')
    objects = PassThroughManager.for_queryset_class(OfficeQuerySet)()
    tags = TaggableManager()

    @cached_property
    def email(self):
        return Email.objects.filter(office=self).order_by('default').first().email

    def __str__(self):
        if not self.visible:
            return _("{name} (hidden)").format(name=self.name)
        return self.name

    def get_absolute_url(self):
        return reverse('offices:detail', kwargs={'slug': self.slug})

    def get_extra_display(self):
        return pformat(self.extra, indent=4)
    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")


@python_2_unicode_compatible
class Email(TimeStampedModel):
    office = models.ForeignKey(Office, verbose_name=_("Office"))
    email = models.EmailField(verbose_name=_("Address"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="office_email")
    valid = models.BooleanField(default=True,
                                verbose_name=_("Is valid?"),
                                help_text=_("Identify if email is valid (still)."))
    default = models.BooleanField(default=True,
                                  verbose_name=_("Default"),
                                  help_text=_("Use this e-mail as primary for office"))

    class Meta:
        verbose_name = _("E-mail address")
        verbose_name_plural = _("E-mail addresses")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "%s?email=%d" % (reverse('cases:create'), self.pk)


def undefault_other(sender, instance, **kwargs):
    if instance.default:
        Email.objects.exclude(pk=instance.pk).filter(office=instance.office).update(default=False)

post_save.connect(undefault_other, sender=Email, dispatch_uid="update_undefault_other")
