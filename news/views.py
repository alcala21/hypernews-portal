from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404, HttpResponse
from datetime import datetime
import json
import random

with open(settings.NEWS_JSON_PATH) as f:
    articles = json.load(f)
# Create your views here.


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        _query = request.GET.get('q')

        _articles = []
        if _query:
            for article in articles:
                if _query.lower() in article['title'].lower():
                    _articles.append(article)
        else:
            _articles = articles[:]

        news_dict = {}
        for article in _articles:
            date_value = article['created'].split(' ')[0]
            if news_dict.get(date_value, 0) == 0:
                news_dict[date_value] = [article]
            else:
                news_dict[date_value].append(article)

        datelist = sorted({x['created'].split(" ")[0] for x in _articles},
                          reverse=True)
        news_list = []
        for _date in datelist:
            date_news = {'created': _date, 'news': news_dict[_date]}
            news_list.append(date_news)

        return render(request, "news/news.html", context={'articles_dict': news_list})


class ArticleView(View):
    def get(self, request, link_id, *args, **kwargs):
        for article in articles:
            if article['link'] == link_id:
                return render(
                    request, 'news/article.html',
                    context=article)
        else:
            raise Http404


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_links = {article["link"] for article in articles}
        link = max(all_links) + 1
        new_article = {'created': created, 'text': text,
                       'title': title, 'link': link}

        articles.append(new_article)

        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(articles, f, indent=2)

        return redirect('/news/')
