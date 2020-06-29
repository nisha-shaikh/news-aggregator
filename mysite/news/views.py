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

def searchView(request):
    return render(request, 'news/index.html')

def listNews(request):
    results = []

    results.extend(getRedditResults())
    results.extend(getNewsAPIResults())

    return JsonResponse(results, safe=False)

def searchNews(request):
    results = []
    if request.method == 'POST':
        keyword = request.POST['kw']

        try:
            # if keyword has already been queried, data will be retrieved from database
            fromDB = SearchRequests.objects.get(pk=keyword)
            entryDate = fromDB.dateAdded

            if entryDate > EXP_DATE:
                results = list(fromDB.searchresults_set.all().values('headline', 'link', 'source'))
            else:
                # if data in database is old, call APIs and save again
                raise AssertionError('old')

        except (SearchRequests.DoesNotExist, AssertionError) as e:
            # save query in database
            reqEntry = SearchRequests(
                query=keyword, dateAdded=datetime.datetime.today().date())
            reqEntry.save()

            if str(e) == 'old':
                # delete old news articles from database
                SearchResults.objects.filter(request=keyword).delete()

            results.extend(searchRedditResults(keyword, reqEntry))
            results.extend(searchNewsAPIResults(keyword, reqEntry))

    return JsonResponse(results, safe=False)

def getRedditResults():
    """
    Gets results from Reddit API with only the fields required
    """
    reddit = praw.Reddit(client_id="4ZQq_6IHGR6t6A",
                             client_secret="AmKTDcjfrcxU6yjpSIu4uY7DvCU",
                             user_agent="testscript by /u/fornewsapi")

        
    results = []

    for submission in reddit.subreddit("news").top(limit=10):
        results.append({
            'headline': submission.title,
            'link': submission.url,
            'source': 'reddit'
        })

    return results

def getNewsAPIResults():
    """
    Gets results from News API with only the fields required
    """
    newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

    results = []

    us_articles = newsapi.get_top_headlines(category="general", page_size=10)

    for news in us_articles['articles']:
        results.append({
            'headline': news['title'],
            'link': news['url'],
            'source': 'newsAPI'
        })

    return results

def searchRedditResults(keyword, reqEntry):
    """
    Searches for results containing keyword from Reddit API with only the fields required
    """
    reddit = praw.Reddit(client_id="4ZQq_6IHGR6t6A",
                             client_secret="AmKTDcjfrcxU6yjpSIu4uY7DvCU",
                             user_agent="testscript by /u/fornewsapi")

        
    results = []

    for submission in reddit.subreddit("news").search(keyword, limit=10):
                submissionDict = {'headline': submission.title,
                                  'link': submission.url,
                                  'source': 'reddit'
                                }
                results.append(submissionDict)

                redditEntry = SearchResults(**submissionDict)
                redditEntry.save()
                redditEntry.request.add(reqEntry)
    return results

def searchNewsAPIResults(keyword, reqEntry):
    """
    Searches for results containing keyword from News API with only the fields required
    """
    newsapi = NewsApiClient(api_key='cb682c4048944cd1a9f17e88bb3ad67f')

    results = []

    for news in newsapi.get_top_headlines(q=keyword, category='general', page_size=10)['articles']:
                newsDict = {'headline': news['title'],
                            'link': news['url'],
                            'source': "newsapi"
                            }
                results.append(newsDict)

                newsEntry = SearchResults(**newsDict)
                newsEntry.save()
                newsEntry.request.add(reqEntry)
    
    return results