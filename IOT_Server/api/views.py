from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Devices, Tags, ValueTypes, IotData
from api.serializers import DeviceSerializer, TagSerializer, ValTypeSerializer
from api.serializers import IotTextSerializer, IotIntegerSerializer, IotDecimalSerializer, IotBooleanSerializer, TagDataSerializer
from rest_framework import generics
from rest_framework.views import APIView


#@api_view(['GET', 'POST'])
#def device_list(request):
#    """
#    List all devices or create a new device
#    """
#    if request.method == 'GET':
#        device_list = Devices.objects.all()
#        serializer = DeviceSerializer(device_list, many=True)
#        return Response(serializer.data)

#    elif request.method == 'POST':
#        serializer = DeviceSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceList(generics.ListCreateAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devices.objects.all()
    serializer_class = DeviceSerializer


class TagList(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer


class ValTypeList(generics.ListCreateAPIView):
    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class ValTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ValueTypes.objects.all()
    serializer_class = ValTypeSerializer


class TagData(APIView):
    def post(self, request, format=None):
        serializer = TagDataSerializer(data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


