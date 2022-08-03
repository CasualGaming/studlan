# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime

from apps.lan.models import LAN
from apps.news.models import Article


def main(request, page):
    active_lans = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    if len(active_lans) > 0:
        articles = Article.objects.filter(relevant_to__in=active_lans).order_by('-pinned', '-pub_date')
    else:
        return redirect('archive_main')

    paginator = Paginator(articles, 10)  # Articles per page

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request, 'news/news.html', {'lans': active_lans, 'articles': articles, 'page': page, 'languages': settings.LANGUAGES})


def single(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'news/single.html', {'article': article})


def archive(request, page):
    try:
        active_lans = LAN.objects.filter(end_date__gte=datetime.now())
        articles = Article.objects.all().exclude(relevant_to__in=active_lans).order_by('-pub_date')
    except TypeError:
        articles = Article.objects.all().order_by('pub_date')
    paginator = Paginator(articles, 10)  # Articles per page
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(request, 'news/archive.html', {'articles': articles, 'page': page, 'languages': settings.LANGUAGES})
