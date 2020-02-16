from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from SimpleNews.models import Picture
# Create your views here.


def image_display(request, pk):
    pic = Picture.objects.get(id=pk)
    return HttpResponse(pic.photo.read(), content_type='image/jpeg')


def pic_upload(request):
    if request.FILES:
        pic = request.FILES['picture'].read()
        Picture(photo=pic).save()
    return HttpResponseRedirect(reverse('pic_list'))


@csrf_exempt
def pic_upload_editormd(request):
    name = request.FILES['editormd-image-file'].name.split('.')
    pic = request.FILES['editormd-image-file'].read()
    pic = Picture(photo=pic, content_type='image/%s' % name[1]).save()
    url = '/api/image/%s' % str(pic.id)
    ans = {'success': 1, 'message': '上传成功', 'url': url}
    return HttpResponse(json.dumps(ans), content_type="application/json")

