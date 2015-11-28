from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import CaseFactory


class CaseListViewTestCase(TestCase):
    def setUp(self):
        self.object_list = CaseFactory.create_batch(50)

    def test_display_objects(self):
        resp = self.assertGoodView('cases:list')
        self.assertContains(resp, self.object_list[0].name)

    def test_display_filter(self):
        resp = self.assertGoodView('cases:list')
        self.assertContains(resp, 'filter')

    def test_query_limit(self):
        with self.assertNumQueriesLessThan(7):
            self.get('cases:list')


class OfficeDetailViewTestCase(TestCase):
    def setUp(self):
        self.object = CaseFactory()

    def test_display_object(self):
        resp = self.client.get(self.object.get_absolute_url())
        self.assertContains(resp, self.object.name)
        self.assertContains(resp, self.object.office)

    def test_display_letters(self):
        pass
        # TODO
