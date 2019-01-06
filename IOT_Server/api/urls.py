#--- IOT_Server - api app urls ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from django.urls import path
from rest_framework.authtoken import views as drf_views
from api import views


urlpatterns = [
    path('device/', views.DeviceList.as_view()),
    path('device/<pk>/', views.DeviceDetail.as_view()),
    path('devicetag/', views.DeviceTagList.as_view()),
    path('devicetag/<device_id>/', views.DeviceTagList.as_view()),
    path('valuetype/', views.ValTypeListCreate.as_view()),
    path('valuetype/<pk>/', views.ValTypeDetail.as_view()),
    path('tag/', views.TagList.as_view()),
    path('tag/<pk>/', views.TagDetail.as_view()),
    path('tagupdate/', views.TagData.as_view()),
    path('tagdata/<tag>/', views.TagDataList.as_view()),
    path('tagcurrent/<tag>/', views.TagDataCurrent.as_view()),
    path('get-api-token/', drf_views.obtain_auth_token),
    ]
