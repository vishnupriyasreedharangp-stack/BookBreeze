from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from products import views


urlpatterns = [
    path(
        '',
        include('products.urls')
    ),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'accounts/signup/',
        views.signup,
        name='signup'
    ),

    path(
        'accounts/logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'admin/',
        admin.site.urls
    ),
]