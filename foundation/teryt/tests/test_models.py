from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import JSTFactory


class TestUser(TestCase):
    def setUp(self):
        self.object = JSTFactory(name="testname")

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/kraj/wojewodztwo-testname'
        )
        level2 = JSTFactory(parent=self.object, name="testname2")
        self.assertEqual(
            level2.get_absolute_url(),
            '/kraj/powiat-testname2'
        )
        level3 = JSTFactory(parent=level2, name="testname3")
        self.assertEqual(
            level3.get_absolute_url(),
            '/kraj/gmina-testname3'
        )
        level4_more = JSTFactory(parent=level3, name="testname4")
        self.assertEqual(
            level4_more.get_absolute_url(),
            '/kraj/region-testname4'
        )
