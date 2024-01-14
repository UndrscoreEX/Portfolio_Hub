from django.contrib import admin
from django.urls import path, include
from portfolio import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('graphic/', views.graphicD, name='graphicD'),
    path('it/', views.it, name='it'),
    path('proffcoaching/', views.personalCoach, name='personalCoach'),
    path('projects/', views.projects, name='projects'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)