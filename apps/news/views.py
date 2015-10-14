#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.news.models import Article
from apps.lan.models import Stream


def main(request, page):
    articles = Article.objects.all()
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
        return render(request, 'news/news.html', {'articles': articles, 'page': page, 'stream': streams[0]})
    else:
        return render(request, 'news/news.html', {'articles': articles, 'page': page})


def single(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'news/single.html', {'article': article})