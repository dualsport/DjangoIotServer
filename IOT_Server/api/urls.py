from django.urls import path
from rest_framework.authtoken import views as drf_views
from api import views


urlpatterns = [
    path('devices/', views.DeviceList.as_view()),
    path('devices/<pk>/', views.DeviceDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<pk>/', views.TagDetail.as_view()),
    path('valuetypes/', views.ValTypeList.as_view()),
    path('valuetypes/<pk>/', views.ValTypeDetail.as_view()),
    path('tagdata/', views.TagData.as_view()),
    path('tagdatalist/', views.TagDataList.as_view()),
    path('get-api-token/', drf_views.obtain_auth_token),
    ]
