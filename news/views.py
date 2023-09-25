
#fbb1270df23a4148a845c82cc0cbc9ed
# news/views.py
from datetime import datetime, timedelta
import requests
from django.shortcuts import render
import pytz

def news_page(request):
    api_key = 'fbb1270df23a4148a845c82cc0cbc9ed'  # Replace with your News API key
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': api_key,
        'country': 'de',  # Germany
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        news_data = response.json()

        berlin_tz = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(berlin_tz)

        # Filter articles by author (Tagesspiegel) and publication time
        tagesspiegel_articles = []
        for article in news_data.get('articles', []):
            # if article.get('author') == 'Tagesspiegel':
                published_at_utc = datetime.strptime(article.get('publishedAt').replace('Z', ''), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.UTC)
                published_at_berlin = published_at_utc.astimezone(berlin_tz)
                if current_time - timedelta(days=1.2) <= published_at_berlin:
                    print(current_time, published_at_berlin)
                    tagesspiegel_articles.append(article)

        return render(request, 'news/news_page.html', {'tagesspiegel_articles': tagesspiegel_articles})
    else:
        error_message = 'Failed to fetch news data'
        return render(request, 'news/error_page.html', {'error_message': error_message})
