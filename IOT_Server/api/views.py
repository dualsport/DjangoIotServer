#--- IOT_Server - api app views ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import View
from django.utils import dateparse
from api.models import Devices, Tags, ValueTypes, IotData
from api.serializers import DeviceSerializer, TagSerializer, TagDataSerializer, ValTypeSerializer, DeviceTagSerializer
from api.permissions import IsOwner, IsSuperUser


class DeviceList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Devices.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer


class TagList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tags.objects.filter(device__owner=self.request.user)


class DeviceTagList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceTagSerializer
    
    def get_queryset(self):
        #Devices owned by request user
        #queryset = Devices.objects.filter(owner=self.request.user) --handled by serializers.OwnedTags
        queryset = Devices.objects.all()
        #Device if given in url
        device = self.kwargs.get('device_id', None)
        if device:
            queryset = queryset.filter(device_id=device)
            if queryset:
                return queryset
            else:
                raise serializers.ValidationError({'Device does not exist': device})
        return queryset

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class ValTypeDispatch(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ValTypeListCreate.as_view()(request, *args, **kwargs)
        else:
            return ValTypeList.as_view()(request, *args, **kwargs)


class ValTypeListCreate(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSuperUser,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer

    #Set name on page
    def get_view_name(self):
        name = 'Value Types'
        suffix = getattr(self, 'suffix', None)
        if suffix:
            name += ' ' + suffix
        return name


class ValTypeList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer

    #Set name on page
    def get_view_name(self):
        name = 'Value Types'
        suffix = getattr(self, 'suffix', None)
        if suffix:
            name += ' ' + suffix
        return name


class ValTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsSuperUser,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class TagData(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = TagDataSerializer(data=request.data, context={'request': request})
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDataList(generics.ListCreateAPIView):
    serializer_class = TagDataSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def validate_date(self, dt):
        valid_dt_fmt = {'Valid date format is': '2010-06-30T15:30:00'}
        try:
            valid_dt = dateparse.parse_datetime(dt)
        except ValueError as e:
            raise serializers.ValidationError({'Invalid date given': str(e)})
        if not valid_dt:
            raise serializers.ValidationError({'Invalid value parameter': f'{dt}',
                                               **valid_dt_fmt})
        return valid_dt


    def get_queryset(self):
        #All IotData owned by request user
        queryset = IotData.objects.filter(tag__device__owner=self.request.user)

        #Filter on tag if given
        req_tag = self.request.query_params.get('tag', None)
        if req_tag:
            queryset = queryset.filter(tag=req_tag)

        #Filter on begin or after if given
        begin = self.request.query_params.get('begin', None)
        after = self.request.query_params.get('after', None)
        if begin or after:
            if begin:
                begin_dt = self.validate_date(begin)
                queryset = queryset.filter(timestamp__gte=begin_dt)
            else:
                after_dt = self.validate_date(after)
                queryset = queryset.filter(timestamp__gt=after_dt)

        #Filter on end or before if given
        end = self.request.query_params.get('end', None)
        before = self.request.query_params.get('before', None)
        if end or before:
            if end:
                end_dt = self.validate_date(end)
                queryset = queryset.filter(timestamp__lte=end_dt)
            else:
                before_dt = self.validate_date(before)
                queryset = queryset.filter(timestamp__lt=before_dt)

        #Limit to max if given, else default to 100 records
        max = int(self.request.query_params.get('max', 100))
        queryset = queryset.order_by('timestamp')[:max]

        return queryset


