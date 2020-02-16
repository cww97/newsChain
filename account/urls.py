from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='account_login'),
    path('logout/', views.logout, name='account_logout'),
    path('<str:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('<str:pk>/pages/', views.AccountPagesListView.as_view(), name='account_pages'),
    path('<str:pk>/settings/', views.settings, name='account_settings'),

]