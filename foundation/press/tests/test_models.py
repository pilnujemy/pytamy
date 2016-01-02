from __future__ import absolute_import
from test_plus.test import TestCase
from .factories import TagFactory, PostFactory


class PostTestCase(TestCase):
    def setUp(self):
        self.object = PostFactory(name="testname")

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/blog/post-testname'
        )


class TagTestCase(TestCase):
    def setUp(self):
        self.object = TagFactory(name="testname")

    def test__str__(self):
        self.assertEqual(
            self.object.__str__(),
            "testname"
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.object.get_absolute_url(),
            '/blog/tag-testname'
        )
