from django.urls import path, include
from . views import (
    home,
    extract,
    products,
    ProductOpinionsView,
    AuthorView,
    charts,
)


urlpatterns = [
    path('', home, name='home'),
    path('extract/', extract, name='extract'),
    path('products/', products, name='products'),
    path('product/<slug>/', ProductOpinionsView.as_view(), name='opinions'),
    path('product/<slug>/charts/$', charts, name='charts'),
    path('author/', AuthorView.as_view(), name='author')
]