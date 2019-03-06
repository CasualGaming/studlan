# -*- coding: utf-8 -*-

from random import SystemRandom

from django.test import TestCase


class TeamTests(TestCase):

    def test_systemrandom_support(self):
        rand = SystemRandom()
        num = rand.randint(510, 515)
        self.assertTrue(num >= 510 and num <= 515)
