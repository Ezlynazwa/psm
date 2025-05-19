# recommendation/urls.py
from django.urls import path
from . import views

app_name = 'recommendation'
urlpatterns = [
    path('recomhome', views.index, name='recomhome'),
]
