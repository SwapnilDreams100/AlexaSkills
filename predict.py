from search import *
import spacy
import retinasdk
# https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz


def predict(claim, source='All'):
    lite_client = retinasdk.LiteClient("2bc45a70-3a85-11e8-9172-3ff24e827f76")
    nlp = spacy.load('en')

    def get_news_titles(claim, keywords):
        kw = keywords
        import itertools
        claim_words = claim.split()
        for i in range(len(keywords)):
            keywords[i] = keywords[i] + " "
        keys_flat = list(itertools.chain(*keywords))
        keywords = ''.join(keys_flat)
        new_claim = ""
        for word in claim_words:
            if word in keywords:
                new_claim = new_claim + " +" + word
            else:
                new_claim = new_claim + " " + word
        print(new_claim)  # Test
        news_titles = []
        if source == 'NewsAPI':
            news_titles = search_news_api(new_claim)
        elif source == 'WebHoseIO':
            news_titles = search_webhoseio(new_claim)
        elif source == 'EventRegistry':
            news_titles = search_event_registry(new_claim)
        else:
            news_api = search_news_api(new_claim)
            if news_api is not None:
                news_titles.append(news_api)
                print('News API = ', news_api)  # Test
            # webhoseio = search_webhoseio(claim)
            # if webhoseio is not None:
            #     news_titles.append(webhoseio)
            #     print('WebhoseIO = ', webhoseio)  # Test
            # event = search_event_registry(claim)
            # if event is not None:
            #     news_titles.append(event)
            #     print('event = ', event)  # Test
            # kwds = '&'.join(list(kw))
            # wikinews = search_wiki_news(claim, kwds)
            # if wikinews is not None:
            #     news_titles.append(wikinews)
            #     print('Wikinews = ', wikinews)
        return news_titles

    keywords = lite_client.getKeywords(claim)
    print(keywords)  # Test
    news = get_news_titles(claim.lower(), keywords)
    print(
        "----------------------------------------------------news--------------------------------------------")  # Test
    if(type(news[0])) != 'str':
        new = []
        for y in news:
            for x in y:
                new.append(x)
        news = new
    print(news)  # Test
    count_agree = 0
    count_disagree = 0
    claim_nlp = nlp(claim)
    for title in news:
        print(title)  # Test
        news_source = nlp(title)
        score = claim_nlp.similarity(news_source)
        print(score)  # Test
        if score > 0.5:
            count_agree += 1
        elif score <= 0.5:
            count_disagree += 1
    if len(news) <= 0:
        return -1
    else:
        probability = (count_agree / (count_agree + count_disagree)) * 100
        print(probability)
        return probability


def check(claim):
    liteClient = retinasdk.LiteClient("2bc45a70-3a85-11e8-9172-3ff24e827f76")
    nlp = spacy.load('en')

    # claim = "Justin Bieber told the bible that the music industry is run by pedophiles"

    def get_news_titles(claim, keywords):
        import itertools
        claim_words = claim.split()
        for i in range(len(keywords)):
            keywords[i] = keywords[i] + " "
        keys_flat = list(itertools.chain(*keywords))
        keywords = ''.join(keys_flat)
        new_claim = ""
        for word in claim_words:
            if word in keywords:
                new_claim = new_claim + " +" + word
            else:
                new_claim = new_claim + " " + word
        print(new_claim)  # Test
        # newsapi = NewsApiClient(api_key='92faf2b60b2e4e4fb15efa42ab950c0f')
        # all_articles = newsapi.get_everything(q=new_claim, language='en', sort_by='relevancy')
        news_api_titles = search_news_api(new_claim)
        return news_api_titles

    keywords = liteClient.getKeywords(claim)
    print(keywords)  # Test
    news = get_news_titles(claim.lower(), keywords)
    print(
        "----------------------------------------------------news--------------------------------------------")  # Test
    print(news)  # Test
    count_agree = 0
    count_disagree = 0
    claim_nlp = nlp(claim)
    for title in news:
        print(title)  # Test
        news_source = nlp(title)
        score = claim_nlp.similarity(news_source)
        print(score)  # Test
        if score > 0.5:
            count_agree += 1
        elif score <= 0.5:
            count_disagree += 1

    if count_agree > count_disagree:
        return "The news seems true according to our sources"
    elif count_agree < count_disagree:
        return "The news seems false according to our sources"
    else:
        return "I am not sure, please try again using different keywords."
