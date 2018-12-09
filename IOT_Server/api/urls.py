from django.urls import path
from api import views


urlpatterns = [
    path('devices/', views.DeviceList.as_view()),
    path('devices/<pk>/', views.DeviceDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<pk>/', views.TagDetail.as_view()),
    path('valuetypes/', views.ValTypeList.as_view()),
    path('valuetypes/<pk>/', views.ValTypeDetail.as_view()),
    path('tagdata/', views.TagData.as_view()),
    ]
