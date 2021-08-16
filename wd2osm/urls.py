from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:catalog_id>/', views.catalog, name="catalog"),
    path('wikidata', views.wikidata, name="wikidata"),
    path('wd', views.wikidata_item, name="wikidata_item")
]