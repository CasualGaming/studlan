#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.datetime_safe import datetime

from apps.news.models import Article
from apps.lan.models import Stream, LAN


def main(request, page):
    active_lans = LAN.objects.filter(end_date__gte=datetime.now())
    articles = Article.objects.filter(relevant_to__in=active_lans).order_by('-pinned', 'pub_date')
    paginator = Paginator(articles, 10) #Articles per page
    streams = Stream.objects.filter(active=True).order_by('-pk')[:1]

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
    if len(streams) > 0:
        return render(request, 'news/news.html', {'articles': articles, 'page': page, 'stream': streams[0], 'languages': settings.LANGUAGES})
    else:
        return render(request, 'news/news.html', {'articles': articles, 'page': page, 'languages': settings.LANGUAGES})


def single(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'news/single.html', {'article': article})