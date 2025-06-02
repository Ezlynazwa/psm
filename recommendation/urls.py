# recommendation/urls.py
from django.urls import path
from . import views
from .views import skin_assessment

app_name = 'recommendation'
urlpatterns = [
    path('recomhome', views.index, name='recomhome'),
    path('skin-assessment/', skin_assessment, name='skin_assessment'),
]
