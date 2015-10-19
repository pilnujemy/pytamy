from __future__ import absolute_import
from .. import models
import factory


class OfficeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'office-/{0}/'.format(n))
    jst = factory.SubFactory('foundation.teryt.tests.factories.JSTFactory')
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')
    verified = True
    state = 'created'

    class Meta:
        model = models.Office


class EmailFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    office = factory.SubFactory(OfficeFactory)
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')

    class Meta:
        model = models.Email
