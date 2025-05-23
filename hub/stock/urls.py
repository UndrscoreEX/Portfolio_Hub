from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stock-info/', views.stock_info, name='stock_info'),
    path('example-result/', views.example_result_view, name='example-result'),
]
