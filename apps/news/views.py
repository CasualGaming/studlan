#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.datetime_safe import datetime

from apps.news.models import Article, FAQ, ToParents
from apps.lan.models import Stream, LAN
from django.core.exceptions import ObjectDoesNotExist


def main(request, page):
    active_lans = LAN.objects.filter(end_date__gte=datetime.now())
    if len(active_lans) > 0:
        articles = Article.objects.filter(relevant_to__in=active_lans).order_by('-pinned', '-pub_date')
    else:
        return redirect('archive')

    paginator = Paginator(articles, 10)  # Articles per page
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
        return render(request, 'news/news.html', {'articles': articles, 'page': page, 'stream': streams[0],
                                                  'languages': settings.LANGUAGES})
    else:
        return render(request, 'news/news.html', {'articles': articles, 'page': page, 'languages':
                                                    settings.LANGUAGES})


def single(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'news/single.html', {'article': article})

def faq(request):
    faq = get_object_or_404(FAQ, active=True)
    return render(request, 'news/single.html', {'article': faq})

def toParents(request):
    toParents = get_object_or_404(ToParents, active=True)
    return render(request, 'news/single.html', {'article': toParents})

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
    except:
        # If no page is given, show the first
        articles = paginator.page(1)
    return render(request, 'news/archive.html', {'articles': articles, 'page': page, 'languages': settings.LANGUAGES})
