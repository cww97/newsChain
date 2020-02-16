from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from SimpleNews.models import *
# Create your views here.
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# ------------------------- views --------------------------------


def login(request):
    if request.method == 'GET':
        return render(request, 'account/account_login.html')
    user = User.objects(username=request.POST['username'])
    if not user: return HttpResponseRedirect(reverse('account_login'))
    request.session['user_id'] = str(user[0].id)
    request.session['username'] = user[0].username
    request.session['user_permission'] = user[0].permission
    return HttpResponseRedirect(reverse('news_list'))


def logout(request):
    if request.session.get('user_id'): del request.session['user_id']
    if request.session.get('username'): del request.session['username']
    if request.session.get('user_permission'): del request.session['user_permission']
    return HttpResponseRedirect(reverse('news_list'))


class AccountDetailView(DetailView):
    model = User
    template_name = 'account/account_detail.html'

    def get_queryset(self):
        return self.model.objects  # (username=self.kwargs.get('pk'))


class AccountPagesListView(ListView):
    model = Page
    template_name = 'account/account_pages.html'
    context_object_name = 'pages'

    def get_queryset(self):
        return self.model.objects(author=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = User.objects.get(id=self.kwargs.get('pk'))
        return context


def settings(request, pk):
    return render(request, 'account/account_settings.html')
