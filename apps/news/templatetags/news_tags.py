# -*- coding: utf-8 -*-

from django import template

from apps.news.models import Article

register = template.Library()


def do_num_of_articles(parser, token):
    return NewsRenderer(len(Article.objects.all()))


class NewsRenderer(template.Node):
    def __init__(self, num_of_articles):
        self.num_of_articles = num_of_articles

    def render(self, context):
        return self.num_of_articles


register.tag('num_of_articles', do_num_of_articles)
