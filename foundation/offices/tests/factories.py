from __future__ import absolute_import
from .. import models
import factory


class OfficeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence('office-/{0}/'.format)
    jst = factory.SubFactory('foundation.teryt.tests.factories.JSTFactory')
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')
    visible = True

    class Meta:
        model = models.Office


class EmailFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence('user-{0}@example.com'.format)
    office = factory.SubFactory(OfficeFactory)
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')
    default = False

    class Meta:
        model = models.Email
