import requests
import json


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
        swapnil_api_key = '92faf2b60b2e4e4fb15efa42ab950c0f'
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
