from django.shortcuts import render
from django.utils.html import escape
from rest_framework.views import APIView
from rest_framework.response import Response
from SimpleNews.models import *
from account.models import User
from django.urls import reverse
from bs4 import BeautifulSoup


def query_user(kw):
    results = list()
    if kw and len(kw) >= 3:
        for user in User.objects(username__contains=kw)[:5]:
            results.append({'title': escape(user.username),
                            'url': reverse('account_detail', kwargs=dict(pk=user.pk))})
    return dict(name='User', results=results)


def query_page(kw, cite=False):
    results = list()
    if kw:
        for page in Page.objects(title__contains=kw, is_final=True)[:5]:
            page_dict = {'title': escape(page.title),
                        'url': reverse('news_detail', kwargs={"pk": page.pk})}
            if cite:
                page_dict['copy'] = '[%s](%s)' % (page_dict['title'], page_dict['url'])
                soup = BeautifulSoup(markdown4.convert(page.content))
                page_dict['has_img'] = True if soup.find('img') else False
                if page_dict['has_img']:
                    image_src = soup.find('img').get('src')
                    page_dict['preview'] = '<img src="%s"/><p>%s<a href="%s">...more</a></p>' % (image_src, page.content[:55], page_dict['url'])
                else:
                    page_dict['preview'] = '<p>%s</p>' % (page.content[:155])
                page_dict['url'] = ''
            results.append(page_dict)
    return dict(name='Pages', results=results)


def query_tag(kw):
    results = list()
    if kw:
        for tag in Tag.objects(name__contains=kw).all()[:5]:
            results.append({'title': escape(tag.name),
                            'url': reverse('tag_page_list',kwargs={'pk': tag.name})})
    return dict(name='Tag', results=results)


class SearchAPI(APIView):
    def get(self, request):
        kw = request.GET.get('kw')
        results = dict()
        if kw:
            results['user'] = query_user(kw)
            results['tag'] = query_tag(kw)
            results['page'] = query_page(kw)
            return Response(dict(results=results, action={
                "url": reverse('search') + '?kw=%s' % kw,
                "text": "View all results"
            }))
        return Response(dict(results=results))


class SearchPageAPI(APIView):
    def get(self, request):
        kw = request.GET.get('kw')
        results = dict()
        if kw:
            results['page'] = query_page(kw, True)
            return Response(dict(results=results, action={
                "url": reverse('search_page') + '?kw=%s' % kw,
                "text": "View all results"
            }))
        return Response(dict(results=results))


