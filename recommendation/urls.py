# recommendation/urls.py

from django.urls import path
from . import views

app_name = 'recommendation'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assessment/', views.take_assessment, name='take_assessment'),
    path('api/recs/', views.api_recommendations, name='api_recs'),
]
