# faq_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the FAQ API homepage!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/faqs/', include('faqs.urls')),
    path('', home, name='home'),  # Home page route
]
