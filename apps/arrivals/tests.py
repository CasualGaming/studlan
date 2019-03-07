# -*- coding: utf-8 -*-

from django.test import TestCase

from .views import flip_string_bool


class ArrivalsTests(TestCase):

    def test_views_flip_string_bool(self):
        self.assertEqual(flip_string_bool('True'), False)
        self.assertEqual(flip_string_bool('False'), True)
        self.assertEqual(flip_string_bool('alpha'), None)
        self.assertEqual(flip_string_bool(''), None)
