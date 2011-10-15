# -*- encoding: utf-8 -*-

from studlan.news.models import Article
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def main(request):
    articles = Article.objects.all()
    return render_to_response('news.html', {'news': articles},
                              context_instance=RequestContext(request))
