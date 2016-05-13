from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation.teryt.models import JST
from django.conf import settings
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from django.db.models.query import QuerySet
from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager
from jsonfield import JSONField
from pprint import pformat


REGON_HELP_TEXT = _("Compatible with National Official Register of National Economy Entities")


class OfficeQuerySet(QuerySet):
    def for_user(self, user):
        if user.has_perm('offices.delete_office'):
            return self
        return self.filter(visible=True)

    def with_case_count(self):
        return self.annotate(case_count=models.Count('case'))

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
    jst = models.ForeignKey(to=JST,
                            verbose_name=_("Unit of administrative division"))
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
    extra = JSONField(default={})
    objects = OfficeQuerySet.as_manager()
    tags = TaggableManager(verbose_name=_("Tags"), blank=True)

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
