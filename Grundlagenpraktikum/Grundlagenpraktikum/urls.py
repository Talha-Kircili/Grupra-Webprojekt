from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views
from django.urls import include, path
from django.shortcuts import redirect
from django.contrib import admin


urlpatterns = [
    path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(template_name="login.html", authentication_form=AuthenticationForm), name='login'),
    path('', include('Praktikum.urls'))
]
