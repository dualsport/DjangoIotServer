from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Devices, Tags, ValueTypes, IotData
from api.serializers import DeviceSerializer, TagSerializer, ValTypeSerializer
from api.serializers import IotTextSerializer, IotIntegerSerializer, IotDecimalSerializer, IotBooleanSerializer, TagDataSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.utils import dateparse
from api.permissions import IsOwner


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

    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class ValTypeList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class ValTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class TagData(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        print(request.data)
        serializer = TagDataSerializer(data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDataList(generics.ListAPIView):
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
        req_tag = self.request.query_params.get('tag', None)
        if req_tag:
            queryset = IotData.objects.filter(tag=req_tag)
        else:
            queryset = IotData.objects.all()

        begin = self.request.query_params.get('begin', None)
        after = self.request.query_params.get('after', None)
        if begin or after:
            if begin:
                begin_dt = self.validate_date(begin)
                queryset = queryset.filter(timestamp__gte=begin_dt)
            else:
                after_dt = self.validate_date(after)
                queryset = queryset.filter(timestamp__gt=after_dt)

        end = self.request.query_params.get('end', None)
        before = self.request.query_params.get('before', None)
        if end or before:
            if end:
                end_dt = self.validate_date(end)
                queryset = queryset.filter(timestamp__lte=end_dt)
            else:
                before_dt = self.validate_date(before)
                queryset = queryset.filter(timestamp__lt=before_dt)

        
        max = int(self.request.query_params.get('max', 100))
        queryset = queryset.order_by('timestamp')[:max]

        return queryset


