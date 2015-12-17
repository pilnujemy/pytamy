from __future__ import absolute_import
from .. import models
import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence('user-{0}'.format)
    email = factory.Sequence('user-{0}@example.com'.format)
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = models.User
        django_get_or_create = ('username', )
