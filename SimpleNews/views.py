from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import *
from .models import *
from api import markdown4
# Create your views here.


class TagListView(ListView):
    model = Tag
    template_name = 'SimpleNews/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return self.model.objects

# -----------------------------Pictures--------------------------


class PictureListView(ListView):
    model = Picture
    template_name = 'SimpleNews/pic_list.html'
    context_object_name = 'pics'

    def get_queryset(self):
        return self.model.objects

# ----------------------------Pages-------------------------------


class NewsListView(ListView):
    model = Page
    template_name = 'SimpleNews/page_list.html'
    # paginate_by = 100
    context_object_name = 'events'

    def get_queryset(self):
        return self.model.objects(is_final=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = list()
        for page in context['events']:
            preview = markdown4.get_preview(page.content)
            context['pages'].append({'news': page,
                                     'preview': preview})
        context['tags'] = Tag.objects
        return context


class TagsPageListView(NewsListView):
    template_name = 'SimpleNews/tag_pages_list.html'

    def get_queryset(self):
        return self.model.objects(tags=self.kwargs.get('pk'), is_final=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('pk')
        return context


class NewsDetailView(DetailView):
    model = Page
    template_name = 'SimpleNews/page_detail.html'

    def get_queryset(self):
        return self.model.objects

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['object']['content'] = markdown4.convert(self.object['content'])
        context['page_author_id'] = str(context['object']['author']['id'])
        for ref in context['object']['ref_list']:
            ref['name'] = Page.objects.get(id=ref['page']).title
        return context


def page_create(request, new_topic=False):
    if request.method == 'GET':
        if request.session.get('username'):
            template = 'SimpleNews/page_create.html'
            if new_topic: template = 'SimpleNews/page_create_new_topic.html'
            return render(request, template)
        return HttpResponseRedirect(reverse('account_login'))
    Page.create(Page(), request=request, original=True)
    if request.POST['action'] == 'submit':
        return HttpResponseRedirect(reverse('news_list'))
    else: return HttpResponseRedirect(
        reverse('account_pages',kwargs={'pk': request.session['user_id']}))


def page_create_new_topic(request):
    return page_create(request,True)


def page_create_with_tag(request, pk):
    if request.session.get('username'):
        return render(request, 'SimpleNews/tag_contribute.html', locals())
    return HttpResponseRedirect(reverse('account_login'))


def page_fork(request, pk):
    if request.method == 'GET':
        if request.session.get('username'):
            page = Page.objects.get(id=pk)
            edit = '%s\n\n---\n\n[%s](/account/%s/),%s,转自[%s](/detail/%s){name=cite cite=derive vote=0}' % (page.content, request.session['username'], request.session['user_id'],datetime.date.today(), page.title, page.id)
            return render(request, 'SimpleNews/page_fork.html', locals())
        return HttpResponseRedirect(reverse('account_login'))
    Page.create(Page(), request=request, original=False)
    return HttpResponseRedirect(reverse('news_list'))


def page_draft_update(request, pk):
    page = Page.objects.get(id=pk)
    if request.method == 'GET':
        assert request.session.get('username') == page.author.username
        edit = page.content
        return render(request, 'SimpleNews/page_update.html', locals())
    Page.create(page, request, True)
    return HttpResponseRedirect(reverse('news_detail', kwargs={"pk": page.id}))


def page_delete(request, pk):
    page = Page.objects.get(id=pk)
    assert request.session['user_permission'] == 'admin' or \
           (request.session['user_id'] == str(page.author.id) and not page.is_final)
    page.delete_with_tags()
    return HttpResponseRedirect(reverse('news_list'))
