#--- IOT_Server - api app views ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import View
from django.utils import dateparse
from rest_framework.authtoken.views import ObtainAuthToken
from api.models import Devices, Tags, ValueTypes, IotData
from api.models import WeatherStations, WeatherData
from api.serializers import DeviceSerializer, TagSerializer, TagDataSerializer, ValTypeSerializer, DeviceTagSerializer
from api.serializers import WxStationSerializer, WxDataSerializer, WxDataCreateSerializer
from api.permissions import IsOwner, IsSuperUser, GetOnlyUnlessIsStaff


class DeviceList(generics.ListAPIView):
    """
    get:
    Returns a list of devices that belong to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Devices.objects.filter(owner=self.request.user)


class DeviceCreate(generics.CreateAPIView):
    """
    post:
    Creates a new device that belongs to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: Returns details for the given device.
    put: Update details for the given device. (requires the complete entity)
    patch: Update details for the given device. (requires only the property to be updated)
    delete: Deletes the given device.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer


class TagList(generics.ListAPIView):
    """
    get:
    Returns a list of Tags that belong to you.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tags.objects.filter(device__owner=self.request.user)


class TagCreate(generics.CreateAPIView):
    """
    post:
    Creates a new tag that belongs to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer


class DeviceTagList(generics.ListAPIView):
    """
    get: Returns a nested representation of Devices and Tags that belong to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeviceTagSerializer
    
    def get_queryset(self):
        queryset = Devices.objects.filter(owner=self.request.user)
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
    """
    get: Returns details for the given tag.
    put: Update details for the given tag. (requires the complete entity)
    patch: Update details for the given tag. (requires only the property to be updated)
    delete: Deletes the given tag.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class ValTypeListCreate(generics.ListCreateAPIView):
    """
    get: Returns a list of ValueTypes
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, GetOnlyUnlessIsStaff,)

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
    """
    get: Returns a list of ValueTypes
    post: Create a new ValueType record
    put: Update details for the given ValueType. (requires the complete entity)
    patch: Update details for the given ValueType. (requires only the property to be updated)
    delete: Deletes the given ValueType.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser,)

    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class TagData(APIView):
    """
    post: Add a new value record for a Tag.
    data
    {
      "tag": "string",
      "value": "string"
    }
    |
    Optional json parameter: "timestamp": "<timezone aware datetime>"
    If optional timestamp is not supplied the current datetime will be used.
    Timezone aware format example: "1999-01-31T09:00:00.000-06:00" (US CST)
    Timezone aware format example: "1999-01-31T15:00:00.000Z" (GMT)
    """
    serializer_class = TagDataSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = TagDataSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDataList(generics.ListAPIView):
    """
    get: Returns a list of data for the given tag.
    |
    Allowable URL parameters are:
    begin=datetime -- Return records from this time (inclusive)
    after=datetime -- Return records after this time (non-inclusive)
    end=datetime -- Return records up to this time (inclusive)
    before=datetime -- Return records occurring before this time (non-inclusive)
    max=number -- Maximum number of records to return (default=100)
    |
    Note1 - all datetime values must be given in timezone aware format, e.g. "2010-01-27T18:09:23.123456Z"
    Note2 - If begin & after are given begin is used, if end and before are given end is used.

    """
    serializer_class = TagDataSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def validate_date(self, dt):
        valid_dt_fmt = {'Valid datetime format is': '2010-06-30T15:30:00'}
        try:
            valid_dt = dateparse.parse_datetime(dt)
        except ValueError as e:
            raise serializers.ValidationError({'Invalid value given': str(e)})
        if not valid_dt:
            raise serializers.ValidationError({'Invalid datetime parameter': f'{dt}',
                                               **valid_dt_fmt})
        return valid_dt


    def get_queryset(self):
        #All IotData owned by request user
        queryset = IotData.objects.filter(tag__device__owner=self.request.user)

        #Filter on tag if given
        req_tag = self.kwargs.get('tag', None)
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


class TagDataCurrent(generics.ListAPIView):
    """
    get: Returns the most recent record for a given tag
    """
    serializer_class = TagDataSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #All IotData owned by request user
        queryset = IotData.objects.filter(tag__device__owner=self.request.user)
        #Filter on tag
        req_tag = self.kwargs.get('tag', None)
        if req_tag:
            queryset = queryset.filter(tag=req_tag)
        else:
            #return the last record of all owned tags
            #could throw a ValidationError here
            pass
        #return last record
        queryset = queryset.order_by('-timestamp')[:1]

        return queryset


class WxStationList(generics.ListAPIView):
    """
    get:
    Returns a list of Weather Stations that belong to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WxStationSerializer

    def get_queryset(self):
        return WeatherStations.objects.filter(owner=self.request.user)


class WxStationCreate(generics.CreateAPIView):
    """
    post:
    Creates a new Weather Station that belongs to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WxStationSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WxStationList(generics.ListAPIView):
    """
    get:
    Returns a list of Weather Stations that belong to you.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WxStationSerializer

    def get_queryset(self):
        return WeatherStations.objects.filter(owner=self.request.user)


class WxStationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    get: Returns details for the given weather station.
    put: Update details for the given weather station. (requires the complete entity)
    patch: Update details for the given weather station. (requires only the property to be updated)
    delete: Deletes the given weather station.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner,)

    queryset = WeatherStations.objects.all()
    serializer_class = WxStationSerializer
    lookup_field = 'identifier'


class WxDataCreate(generics.CreateAPIView):
    """
    post:
    Creates a new Weather data record
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WxDataCreateSerializer

    def post(self, request, format=None):
        serializer = WxDataCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WxDataList(generics.ListAPIView):
    """
    get:
    Returns a list of Weather data for a given station id.
    |
    Allowable URL parameters are:
    begin=datetime -- Return records from this time (inclusive)
    after=datetime -- Return records after this time (non-inclusive)
    end=datetime -- Return records up to this time (inclusive)
    before=datetime -- Return records occurring before this time (non-inclusive)
    max=number -- Maximum number of records to return (default=100)
    |
    Note1 - all datetime values must be given in timezone aware format, e.g. "2010-01-27T18:09:23.123456Z"
    Note2 - If begin & after are given begin is used, if end and before are given end is used.

    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WxDataSerializer

    def validate_date(self, dt):
        valid_dt_fmt = {'Valid datetime format is': '2010-06-30T15:30:00'}
        try:
            valid_dt = dateparse.parse_datetime(dt)
        except ValueError as e:
            raise serializers.ValidationError({'Invalid value given': str(e)})
        if not valid_dt:
            raise serializers.ValidationError({'Invalid datetime parameter': f'{dt}',
                                               **valid_dt_fmt})
        return valid_dt

    def get_queryset(self):
        req_identifier = self.kwargs.get('identifier', None)
        station_exists = WeatherStations.objects.filter(owner=self.request.user,
                                                        identifier=req_identifier).count()
        if not station_exists:
             raise serializers.ValidationError({'Station identifier does not exist': req_identifier})

        queryset = WeatherData.objects.filter(station__owner=self.request.user,
                                              station__identifier=req_identifier)

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


class WxDataCurrent(generics.ListAPIView):
    """
    get: Returns the most recent record for a given station id.
    """
    serializer_class = WxDataSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        req_identifier = self.kwargs.get('identifier', None)
        station_exists = WeatherStations.objects.filter(owner=self.request.user,
                                                        identifier=req_identifier).count()
        if not station_exists:
             raise serializers.ValidationError({'Station identifier does not exist': req_identifier})

        queryset = WeatherData.objects.filter(station__owner=self.request.user,
                                              station__identifier=req_identifier)

        queryset = queryset.order_by('-timestamp')[:1]

        return queryset


    