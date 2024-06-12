from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('shopify_authenticate/', views.shopify_authenticate, name='shopify_authenticate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
