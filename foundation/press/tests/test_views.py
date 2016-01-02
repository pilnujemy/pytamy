from __future__ import absolute_import
from datetime import datetime
from test_plus.test import TestCase
from .factories import TagFactory, PostFactory
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.timezone import utc


class PostArchiveMixin(object):
    def test_display_object(self):
        resp = self.assertGoodView(self.url)
        self.assertContains(resp, self.object.name)


class PostArchiveIndexViewTestCase(TestCase):
    url = reverse_lazy('press:archive')

    def setUp(self):
        self.object_list = PostFactory.create_batch(30)
        self.object_list.sort(key=lambda x: x.published, reverse=True)
        self.object = self.object_list[0]

    def test_pagination(self):
        resp = self.assertGoodView(self.url)
        self.assertNotContains(resp, self.object_list[29].name)

    def test_query_limit(self):
        with self.assertNumQueriesLessThan(7):
            self.client.get(self.url)


class PostYearArchiveViewTestCase(PostArchiveMixin, TestCase):
    def setUp(self):
        self.object = PostFactory(published=datetime(2016, 1, 2, tzinfo=utc))
        self.url = reverse('press:archive', kwargs={'year': 2016})


class PostMonthArchiveViewTestCase(PostArchiveMixin, TestCase):
    def setUp(self):
        self.object = PostFactory(published=datetime(2016, 1, 2, tzinfo=utc))
        self.url = reverse('press:archive', kwargs={'year': 2016,
                                                    'month': 1})


class PostDayArchiveViewTestCase(PostArchiveMixin, TestCase):
    def setUp(self):
        self.object = PostFactory(published=datetime(2016, 1, 2, tzinfo=utc))
        self.url = reverse('press:archive', kwargs={'year': 2016,
                                                    'month': 1,
                                                    'day': 2})


class PostTagViewTestCase(PostArchiveMixin, TestCase):
    def setUp(self):
        self.tag = TagFactory(name="example-name")
        self.object = PostFactory(published=datetime(2016, 1, 2, tzinfo=utc),
                                  tags=[self.tag])
        self.url = reverse('press:archive', kwargs={'slug': 'example-name'})

    def test_display_tag(self):
        resp = self.assertGoodView(self.url)
        self.assertContains(resp, self.tag.name)
