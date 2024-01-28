from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls') ),
    path('bach/', include('bach_calc.urls')),
    path('image/', include('ai_gen.urls')),
    path('/', include('portfolio.urls') ),

]
