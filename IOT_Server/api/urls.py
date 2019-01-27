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
    path('device/tags/', views.DeviceTagList.as_view()),
    path('device/tags/<device_id>/', views.DeviceTagList.as_view()),
    path('valuetype/', views.ValTypeListCreate.as_view()),
    path('valuetype/<pk>/', views.ValTypeDetail.as_view()),
    path('tag/add/', views.TagCreate.as_view()),
    path('tag/edit/<pk>/', views.TagDetail.as_view()),
    path('tag/list/', views.TagList.as_view()),
    path('data/add/', views.TagData.as_view()),
    path('data/list/<tag>/', views.TagDataList.as_view()),
    path('data/current/<tag>/', views.TagDataCurrent.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    ]


schema_view = get_swagger_view(title="Swagger Docs", patterns=urlpatterns_include)

#Only urls in urlpatterns_include are included in Swagger documentation
urlpatterns = urlpatterns_include + [
    path('docs/', schema_view),
    ]