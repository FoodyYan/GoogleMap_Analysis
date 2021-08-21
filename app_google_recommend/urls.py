from django.urls import path
from app_google_recommend import views

app_name = 'app_google_recommend'

urlpatterns = [
    path('', views.chart_cate_topword, name='chart_topword'),
    path('api_get_cate_topword/', views.api_get_cate_topword, name='api_cate_topword'),
    path('api_get_cate_info/', views.api_get_cate_info, name='api_get_cate_info'),
]
