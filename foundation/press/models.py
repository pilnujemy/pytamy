from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from model_utils.models import TimeStampedModel
from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('press:archive', kwargs={'slug': self.slug})


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published__lte=now())


@python_2_unicode_compatible
class Post(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=150)
    slug = AutoSlugField(populate_from='name', unique=True, verbose_name=_("Slug"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    published = models.DateTimeField(null=True,
                                     blank=True,
                                     verbose_name=_("Published date"),
                                     db_index=True)
    excerpt = RichTextField(blank=True)
    body = RichTextField(blank=True)
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('press:details', kwargs={'slug': self.slug})
