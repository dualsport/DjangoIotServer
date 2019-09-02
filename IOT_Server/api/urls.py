#--- IOT_Server - api app urls ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from api import views
from rest_framework_swagger.views import get_swagger_view


urlpatterns_include = [
    path('device/add/', views.DeviceCreate.as_view()),
    path('device/edit/<pk>/', views.DeviceDetail.as_view()),
    path('device/list/', views.DeviceList.as_view()),
    path('device/tag/', views.DeviceTagList.as_view()),
    path('device/tag/<device_id>/', views.DeviceTagList.as_view()),
    path('valuetype/', views.ValTypeListCreate.as_view()),
    path('valuetype/<pk>/', views.ValTypeDetail.as_view()),
    path('tag/add/', views.TagCreate.as_view()),
    path('tag/edit/<pk>/', views.TagDetail.as_view()),
    path('tag/list/', views.TagList.as_view()),
    path('data/add/', views.TagData.as_view()),
    path('data/list/<tag>/', views.TagDataList.as_view()),
    path('data/current/<tag>/', views.TagDataCurrent.as_view()),
    path('weatherstation/add/', views.WxStationCreate.as_view()),
    path('weatherstation/edit/<identifier>/', views.WxStationDetail.as_view()),
    path('weatherstation/list/', views.WxStationList.as_view()),
    path('weatherdata/add/', views.WxDataCreate.as_view()),
    path('weatherdata/list/<station>', views.WxDataList.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    ]


schema_view = get_swagger_view(title="Red Cat IOT Docs", patterns=urlpatterns_include)

#Only urls in urlpatterns_include are included in Swagger documentation
urlpatterns = urlpatterns_include + [
    path('', schema_view),
    path('docs/', schema_view),
    ]