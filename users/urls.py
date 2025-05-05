# users/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'
urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.customer_profile, name='customer_profile'),
]

    # You can add more URLs for other views in this app
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
