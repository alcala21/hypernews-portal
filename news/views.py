from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import Http404
import json




# Create your views here.
class NewsView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'news/index.html'
            )


class ArticleView(View):
    def get(self, request, link_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH) as f:
            articles = json.load(f)

        for article in articles:
            print(article['link'], link_id)
            if article['link'] == link_id:
                return render(
                    request, 'news/article.html',
                    context=article)
        else:
            raise Http404


