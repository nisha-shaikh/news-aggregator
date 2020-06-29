import datetime
import json

from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from newsapi import NewsApiClient
import praw

from .models import SearchRequests, SearchResults

# Create your views here.

#TODO: pagination
#TODO: formatting

EXP_DATE = datetime.date(2020, 1, 1)


def listNews(request):
    results = []

    reddit = praw.Reddit(client_id="4ZQq_6IHGR6t6A",
                         client_secret="AmKTDcjfrcxU6yjpSIu4uY7DvCU",
                         user_agent="testscript by /u/fornewsapi")

    for submission in reddit.subreddit("news").top(limit=10):
        results.append({
            'headline': submission.title,
            'link': submission.url,
            'source': 'reddit'
        })

    newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

    us_articles = newsapi.get_top_headlines(category="general", page_size=10)

    for news in us_articles['articles']:
        results.append({
            'headline': news['title'],
            'link': news['url'],
            'source': 'newsapi'
        })

    # results = {}

    # all_articles = newsapi.get_everything(q='tech')
    # for i, item in enumerate(all_articles['articles']):
    #     results[i] = item

    # context = {
    #     'results': results
    # }

    return render(request, 'news/index.html')
    # return JsonResponse(results, safe=False)


def searchNews(request):
    if request.method == 'POST':
        reddit = praw.Reddit(client_id="4ZQq_6IHGR6t6A",
                             client_secret="AmKTDcjfrcxU6yjpSIu4uY7DvCU",
                             user_agent="testscript by /u/fornewsapi")

        newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

        keyword = request.POST['kw']

        results = []

        try:
            fromDB = SearchRequests.objects.get(pk=keyword)
            print('from db')
            entryDate = fromDB.dateAdded
            if entryDate > EXP_DATE:
                dbResults = list(fromDB.searchresults_set.all().values('headline', 'link', 'source'))
                return JsonResponse(dbResults, safe=False)
        except SearchRequests.DoesNotExist:
            print('from api')
            reqEntry = SearchRequests(
                query=keyword, dateAdded=datetime.datetime.today().date())
            reqEntry.save()

            for submission in reddit.subreddit("news").search(keyword, limit=10):
                submissionDict = {'headline': submission.title,
                                  'link': submission.url,
                                  'source': 'reddit'
                                }
                results.append(submissionDict)

                redditEntry = SearchResults(**submissionDict)
                redditEntry.save()
                redditEntry.request.add(reqEntry)

            for news in newsapi.get_top_headlines(q=keyword, category='general', page_size=10)['articles']:
                newsDict = {'headline': news['title'],
                            'link': news['url'],
                            'source': "newsapi"
                            }
                results.append(newsDict)

                newsEntry = SearchResults(**newsDict)
                newsEntry.save()
                newsEntry.request.add(reqEntry)

        return JsonResponse(results, safe=False)
