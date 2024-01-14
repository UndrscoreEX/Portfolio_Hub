from django.urls import path
from .views import Calculate_spec, Calculate_spec_jp, Stats_en, Stats_jp


urlpatterns =[
    path('eng/', Calculate_spec.as_view(), name='index_eng'),
    path('jp/', Calculate_spec_jp.as_view(), name='index_jp'),
    path('eng/conclusion/', Calculate_spec.as_view(), name='conclusion_eng'),
    path('eng/stats/', Stats_en.as_view(), name='stats_eng'),
    path('jp/conclusion/', Calculate_spec_jp.as_view(), name='conclusion_jp'),
    path('jp/stats/', Stats_jp.as_view(), name='stats_jp'),
]
