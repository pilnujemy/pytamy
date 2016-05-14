from __future__ import absolute_import
from .. import models
import factory
from foundation.offices.tests.factories import OfficeFactory


class EmailFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence('user-{0}@example.com'.format)
    office = factory.SubFactory(OfficeFactory)
    created_by = factory.SubFactory('foundation.users.tests.factories.UserFactory')

    class Meta:
        model = models.Email
