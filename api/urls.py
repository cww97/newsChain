from django.urls import path
from .markdown3 import markdown_convert_api
from . import views, search

urlpatterns = [
    path('markdown/', markdown_convert_api),

    # image
    path('image/<str:pk>/', views.image_display, name='pic'),
    path('image/upload/', views.pic_upload, name='pic_upload'),
    path('image/upload/editor/', views.pic_upload_editormd, name='editor_upload'),

    # search
    path('search/', search.SearchAPI.as_view(), name='search'),
    path('search/page/', search.SearchPageAPI.as_view(), name='search_page'),
]