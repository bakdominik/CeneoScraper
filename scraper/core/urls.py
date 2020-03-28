from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('extract', views.extract, name='extract'),
    path('products', views.products, name='products'),
    path('product/<slug>/', views.ProductOpinionsView.as_view(), name='opinions'),
]