from django.urls import path
from rest_framework.authtoken import views as drf_views
from api import views


urlpatterns = [
    path('devices/', views.DeviceList.as_view()),
    path('device/<pk>/', views.DeviceDetail.as_view()),
    path('devicetags/', views.DeviceTagList.as_view()),
    path('devicetag/<device_id>/', views.DeviceTagList.as_view()),
    path('valuetypes/', views.ValTypeDispatch.as_view()),
    path('valuetype/<pk>/', views.ValTypeDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tag/<pk>/', views.TagDetail.as_view()),
    path('tagupdate/', views.TagData.as_view()),
    path('tagdata/', views.TagDataList.as_view()),
    path('get-api-token/', drf_views.obtain_auth_token),
    ]
