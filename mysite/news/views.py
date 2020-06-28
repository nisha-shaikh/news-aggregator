import datetime
import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from newsapi import NewsApiClient
from collections import ChainMap

# Create your views here.


def listNews(request):
    # newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

    # results = {}

    # all_articles = newsapi.get_everything(q='tech')
    # for i, item in enumerate(all_articles['articles']):
    #     results[i] = item

    # context = {
    #     'results': results
    # }

    return render(request, 'news/index.html')


def searchNews(request):
    if request.method == 'POST':
        newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

        keyword = request.POST['kw']
        lang = request.POST['lang']
        sortBy = request.POST['sort']
        fromDate = request.POST['from']
        to = request.POST['to']

        if to=="":
            to = str(datetime.datetime.today()).split()[0]
        if fromDate=="":
            fromDate=None
        if lang == "":
            lang=None

        results = []

        for i in newsapi.get_everything(q=keyword, from_param=fromDate, to=to, language=lang, sort_by=sortBy)['articles']:
            results.append({
                'Headline': i['title'],
                'Link': i['url'],
                'Source': i['source']['name'],
                'Published at': i['publishedAt']
            })

        return JsonResponse(newsapi.get_everything(q=keyword, from_param=fromDate, to=to, language=lang, sort_by=sortBy)['articles'], safe=False)
