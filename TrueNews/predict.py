from search import *
import retinasdk
import paralleldots

paralleldots.get_api_key()

def predict(claim, source='All'):
    lite_client = retinasdk.LiteClient("2bc45a70-3a85-11e8-9172-3ff24e827f76")

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
        news_titles = []
        news_api = search_news_api(new_claim)
        if news_api is not None:
            news_titles.append(news_api)
        return news_titles

    keywords = lite_client.getKeywords(claim)
    news = get_news_titles(claim.lower(), keywords)
    if(type(news[0])) != 'str':
        new = []
        for y in news:
            for x in y:
                new.append(x)
        news = new
    count_agree = 0
    count_disagree = 0
    for title in news:
        
        test_sim=paralleldots.similarity(claim, title)
        score=test_sim["actual_score"]
        if score > 0.5:
            count_agree += 1
        elif score <= 0.5:
            count_disagree += 1
    if len(news) <= 0:
        return -1
    else:
        probability = (count_agree / (count_agree + count_disagree)) * 100
        return probability
