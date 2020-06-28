import datetime
import json
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from newsapi import NewsApiClient
import praw

# Create your views here.

#TODO: pagination
#TODO: formatting

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
            'source': 'newsAPI'
        })

    # results = {}

    # all_articles = newsapi.get_everything(q='tech')
    # for i, item in enumerate(all_articles['articles']):
    #     results[i] = item

    # context = {
    #     'results': results
    # }

    # return render(request, 'news/index.html')
    return JsonResponse(results, safe=False)


def searchNews(request):
    if request.method == 'POST':
        reddit = praw.Reddit(client_id="4ZQq_6IHGR6t6A",
                            client_secret="AmKTDcjfrcxU6yjpSIu4uY7DvCU",
                            user_agent="testscript by /u/fornewsapi")

        for submission in reddit.subreddit("news").hot(limit=10):
            print(submission.title)

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
