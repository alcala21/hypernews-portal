from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import Http404, HttpResponse
import json

with open(settings.NEWS_JSON_PATH) as f:
    articles = json.load(f)
# Create your views here.


class BaseView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/index.html'
        )


class NewsView(View):
    def get(self, request, *args, **kwargs):
        news_dict = {}
        for article in articles:
            date_value = article['created'].split(' ')[0]
            if news_dict.get(date_value, 0) == 0:
                news_dict[date_value] = [article]
            else:
                news_dict[date_value].append(article)

        datelist = sorted({x['created'].split(" ")[0] for x in articles},
                          reverse=True)
        news_list = []
        for _date in datelist:
            date_news = {'created': _date, 'news': news_dict[_date]}
            news_list.append(date_news)

        return render(request, "news/news.html", context={
            'articles_dict': news_list
        })


class ArticleView(View):
    def get(self, request, link_id, *args, **kwargs):
        for article in articles:
            if article['link'] == link_id:
                return render(
                    request, 'news/article.html',
                    context=article)
        else:
            raise Http404
