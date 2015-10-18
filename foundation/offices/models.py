from django.db import models
from django.utils.translation import ugettext as _
from foundation.teryt.models import JST
from django.conf import settings
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from autoslug import AutoSlugField
from django_states.fields import StateField
from django_states.machine import StateMachine, StateDefinition, StateTransition


class OfficeStateMachine(StateMachine):
    log_transitions = True

    # possible states
    class created(StateDefinition):
        description = _('Office created')
        initial = True

    class accepted(StateDefinition):
        description = _('Accepted')

    class destroyed(StateDefinition):
        description = _('Destroyed')

    # state transitions
    class accept(StateTransition):
        from_state = 'created'
        to_state = 'accepted'
        description = _('Mark this office as accepted')

        def handler(transition, instance, user):
            instance.verified = True
            instance.save()

    class destroy(StateTransition):
        from_state = 'accepted'
        to_state = 'destroyed'
        description = _('Mark this office as destroyed')


class OfficeQuerySet(QuerySet):
    def for_user(self, user):
        return self


class Office(TimeStampedModel):
    name = models.CharField(max_length=150, verbose_name=_("Name"))
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = models.ManyToManyField('self')
    jst = models.ForeignKey(JST)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    verified = models.BooleanField(default=False, verbose_name=_("Verified"))
    state = StateField(machine=OfficeStateMachine, default='created')
    objects = PassThroughManager.for_queryset_class(OfficeQuerySet)()

    def __unicode__(self):
        if self.state is 'destroyed':
            return _("{name} (destroyed)").format(name=self.name)
        if not self.verified:
            return _("{name} (unverified)").format(name=self.name)
        return self.name

    def get_absolute_url(self):
        return reverse('offices:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _("Office")
        verbose_name_plural = _("Offices")


class Email(models.Model):
    office = models.ForeignKey(Office, verbose_name=_("Office"))
    email = models.EmailField(verbose_name=_("Address"))
    default = models.BooleanField(default=True, verbose_name=_("Default"),
                                  help_text=_("Use this e-mail as primary for office"))

    class Meta:
        verbose_name = _("E-mail address")
        verbose_name_plural = _("E-mail addresses")
