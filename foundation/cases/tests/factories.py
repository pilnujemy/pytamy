from __future__ import absolute_import
from .. import models
import factory


class CaseFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'case-/{0}/'.format(n))
    office = factory.SubFactory('foundation.offices.tests.factories.OfficeFactory')
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')

    class Meta:
        model = models.Case
