from django.urls import path

from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('pics/', views.PictureListView.as_view(), name='pic_list'),
    path('detail/<str:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('create/', views.page_create, name='news_create'),
    path('create/<str:pk>/', views.page_create_with_tag, name='tag_contribute'),
    path('new_topic/', views.page_create_new_topic, name='new_topic'),
    path('fork/<str:pk>/', views.page_fork, name='news_fork'),
    path('update/<str:pk>/', views.page_draft_update, name='draft_update'),
    path('delete/<str:pk>/', views.page_delete, name='news_delete'),

    # tags
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<str:pk>', views.TagsPageListView.as_view(), name='tag_page_list'),
]