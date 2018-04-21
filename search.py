import requests
import json
import webhoseio
from eventregistry import *


def search_news_api(query, strict=False):
    url = ('https://newsapi.org/v2/everything?'
           'q=' + query + '&'
                          'sortBy=relevancy&'
                          'language=en&'
                          'apiKey=bc37eb8c28b84f7c93c6b353762751f2')
    try:
        response = requests.get(url)
        ans = response.json()
        status = ans['status']
        if status == 'error':
            raise ValueError()
    except ValueError:
        swapnil_api_key = '92faf2b60b2e4e4fb15efa42ab950c0f'  # Check  # Swapnil
        url = ('https://newsapi.org/v2/everything?'
               'q=' + query + '&'
                              'sortBy=relevancy&'
                              'language=en&'
                              'apiKey=' + swapnil_api_key)
        response = requests.get(url)
        ans = response.json()
    i = 0
    titles = []
    match = []
    while True:
        try:
            t = ans['articles'][i]['title']
            titles.append(t)
            if query in t:
                match.append(t)
            i += 1
        except Exception:
            break
    if strict:
        return match
    else:
        return titles


def search_webhoseio(query, strict=False):
    webhoseio.config(token='490f1b67-2a40-433d-922a-11dd051cefb2')
    query_params = {
        "q": "\"" + query + "\" "
        "language:english ",
        "sort": "relevancy",
    }
    try:
        output = webhoseio.query("filterWebContent", query_params)
    except Exception:
        swapnil_token = 'c4d74570-f22c-4d15-8190-880ef716eb91'
        webhoseio.config(token=swapnil_token)
        output = webhoseio.query("filterWebContent", query_params)

    i = 0
    titles = []
    match = []
    while True:
        try:
            t = output['posts'][i]['thread']['title']
            titles.append(t)
            if query in t:
                match.append(t)
            i += 1
        except Exception:
            break
    if strict:
        return match
    else:
        return titles


def search_event_registry(query, strict=False):
    er = EventRegistry(apiKey='7b97ebd9-64d6-4289-9491-7ce56ad4ae55')
    # q = QueryArticlesIter(conceptUri=er.getConceptUri(query), lang="eng")
    q = QueryArticlesIter(keywords=query, lang="eng")
    try:
        articles = q.execQuery(er, sortBy='rel')
    except Exception:
        swapnil_api_key = ''  # Check  # Swapnil
        er = EventRegistry(apiKey=swapnil_api_key)
        articles = q.execQuery(er, sortBy='rel')
    titles = []
    match = []
    for article in articles:
        t = article['title']
        titles.append(t)
        if query in t:
            match.append(t)
    if strict:
        return match
    else:
        return titles


def search_news_api2(query, strict=False):
    url = ('https://newsapi.org/v2/everything?'
           'q=' + query + '&'
                          'sortBy=relevancy&'
                          'sources=google-news&'
                          'language=en&'
                          'pageSize=10&'
                          'apiKey=bc37eb8c28b84f7c93c6b353762751f2')
    try:
        response = requests.get(url)
        ans = response.json()
        status = ans['status']
        if status == 'error':
            raise ValueError()
    except ValueError:
        swapnil_api_key = '92faf2b60b2e4e4fb15efa42ab950c0f'  # Check  # Swapnil
        url = ('https://newsapi.org/v2/everything?'
               'q=' + query + '&'
                              'sortBy=relevancy&'
                              'sources=google-news&'
                              'language=en&'
                              'pageSize=10&'
                              'apiKey=' + swapnil_api_key)
        response = requests.get(url)
        ans = response.json()
    i = 0
    titles = []
    match = []
    while True:
        try:
            t = ans['articles'][i]['title']
            titles.append(t)
            if query in t:
                match.append(t)
            i += 1
        except Exception:
            break
    if strict:
        return match
    else:
        return titles


def search_wiki_news(query, keywords):
    url = "https://en.wikinews.org/w/api.php?"
    parameters = {
        "action": "query",
        "format": "json",
        "list": "search",
        "redirects": 1,
        "srsearch": query + " intitle:"+keywords,
        "srnamespace": "*",
        "srlimit": "500",
        "srenablerewrites": 1
    }
    page = requests.get(url, params=parameters)
    dictionary_news = page.json()
    titles = []
    print("-------------WikiNews-------------")  # Test
    for i in range(len(dictionary_news['query']['search'])):
        title = dictionary_news['query']['search'][i]['title']
        print(title)
        if not (title.startswith('File:') or title.startswith('Thread:Comments:') or title.startswith(
                'Category:') or title.startswith('Talk:') or title.startswith('Comments:')):
            titles.append(title)
            print(title)  # Test
    print('\n\n\n\n')  # Test
