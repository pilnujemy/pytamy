from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import JSTFactory
from foundation.offices.tests.factories import OfficeFactory


class JSTListViewTestCase(TestCase):
    def setUp(self):
        self.object_list = JSTFactory.create_batch(50)

    def test_display_objects(self):
        resp = self.assertGoodView('teryt:list')
        self.assertContains(resp, self.object_list[0].name)

    def test_display_filter(self):
        resp = self.assertGoodView('teryt:list')
        self.assertContains(resp, 'filter')

    def test_query_limit(self):
        with self.assertNumQueriesLessThan(7):
            self.get('teryt:list')


class JSTDetailViewTestCase(TestCase):
    def setUp(self):
        self.object = JSTFactory()

    def test_display_object(self):
        resp = self.client.get(self.object.get_absolute_url())
        self.assertContains(resp, self.object.name)

    def test_display_office(self):
        obj = OfficeFactory(jst=self.object)
        resp = self.client.get(self.object.get_absolute_url())
        self.assertContains(resp, obj.name)
        self.assertContains(resp, obj.get_absolute_url())
