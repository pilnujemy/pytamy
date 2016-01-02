from __future__ import absolute_import
from .. import models
import factory
import factory.fuzzy
from django.utils.timezone import now, utc
from datetime import datetime


class PostFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    user = factory.SubFactory('foundation.users.tests.factories.UserFactory')
    published = factory.fuzzy.FuzzyDateTime(start_dt=datetime(2008, 1, 1, tzinfo=utc),
                                            end_dt=now())
    excerpt = factory.fuzzy.FuzzyText()
    body = factory.fuzzy.FuzzyText()

    class Meta:
        model = models.Post

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()

    class Meta:
        model = models.Tag
