#!/usr/bin/python
# -*- coding: utf-8 -*-

from studlan.news.models import Article
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    objects = Article.objects.all()
    paginator = Paginator(objects, 10)

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:

        # If page is not an integer, deliver first page.

        articles = paginator.page(1)
    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.

        articles = paginator.page(paginator.num_pages)
    except:

        # If no page is given, show the first

        articles = paginator.page(1)

    return render_to_response('news.html', {'news': articles},
                              context_instance=RequestContext(request))
