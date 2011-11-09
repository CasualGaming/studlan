# -*- encoding: utf-8 -*-

from studlan.news.models import Article
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

def main(request):
    articles = Article.objects.all()
    state = "Please log in below"
    return render_to_response('news.html', {'state':state, 'news':articles},
                              context_instance=RequestContext(request))

