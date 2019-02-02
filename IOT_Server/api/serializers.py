#--- IOT_Server - api app serializers ----------------------------------------------
#--- Original Release: December 2018
#--- By: Conrad Eggan
#--- Email: Conrade@RedCatMfg.com

from rest_framework import serializers
from api.models import Devices, Tags, ValueTypes, IotData
from distutils.util import strtobool


class DeviceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Devices
        fields = ('device_id', 'owner', 'name', 'description', 'type')


class OwnedDevices(serializers.PrimaryKeyRelatedField):
    #Limit device list to those owned by request.user
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Devices.objects.filter(owner=user)
        return queryset


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    device = OwnedDevices(many=False)
    class Meta:
        model = Tags
        fields = ('tag_id', 'owner', 'name', 'description', 'device', 'value_type')


class DeviceTags(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag_id', 'name', 'description', 'value_type')


class DeviceTagSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    device_tags = DeviceTags(many=True, read_only=True)

    class Meta:
        model = Devices
        fields = ('device_id', 'owner', 'name', 'description', 'type', 'device_tags')


class ValTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueTypes
        fields = ('value_type_id', 'name', 'type')


class OwnedTags(serializers.PrimaryKeyRelatedField):
    #Limit tag list to those owned by request.user
    def get_queryset(self):
        user = self.context['request'].user
        queryset = Tags.objects.filter(device__owner=user)
        return queryset


class TagDataSerializer(serializers.ModelSerializer):
    value = serializers.CharField(max_length=100)
    type = serializers.ReadOnlyField(source='tag.value_type.type')
    owner = serializers.ReadOnlyField(source='owner.username')
    tag = OwnedTags(many=False)

    class Meta:
        model = IotData
        fields = ('tag','owner','type','value','timestamp')

    def to_internal_value(self, data):
        values = super().to_internal_value(data)

        #Get value type for tag POSTED
        tag_type = Tags.objects.select_related('value_type').get(pk=data['tag']).value_type.type
        
        val = str(data['value'])

        #-- Save value POSTED in appropriate field based on tag value type --
        #Handle boolean value
        if tag_type == 'bool':
            try:
                values['value_bool'] = strtobool(val)
            except ValueError:
                msg = 'Boolean value required. (True, Yes, Y, On, 1, False, No, N, Off, 0)'
                raise serializers.ValidationError({data['tag']: msg})

        #Handle integer value
        elif tag_type == 'int':
            try:
                int(val)
                values['value_int'] = val
            except ValueError:
                raise serializers.ValidationError({data['tag']: 'Integer value required.'})
        
        #Handle decimal value
        elif tag_type == 'dec':
            try:
                float(val)
            except ValueError:
                raise serializers.ValidationError({data['tag']: 'Numeric value required.'})
            #check lengths of decimal number parts
            digit_max = IotData._meta.get_field('value_dec').max_digits
            dec_max = IotData._meta.get_field('value_dec').decimal_places
            if '.' in val:
                val_parts = val.split('.')
            else:
                val_parts = (val, "0")
            if len(val_parts[0]) > digit_max - dec_max:
                msg = f'Maximum of {digit_max-dec_max} digits before the decimal point exceeded.'
                raise serializers.ValidationError({data['tag']: msg})
            if len(val_parts[1]) > dec_max:
                msg = f'Maximum of {dec_max} digits after the decimal point exceeded.'
                raise serializers.ValidationError({data['tag']: msg})
            values['value_dec'] = val

        #Handle string value
        elif tag_type == 'string':
            values['value_text'] = val

        else:
            msg = f'ValueType not defined.'
            raise serializers.ValidationError({data['tag']: msg})

        del values['value']
        return values

    #Validate request.user is owner of tag
    def validate_tag(self, value):
        if self.context['request'].user != value.owner:
            msg = f"""Invalid pk "{value.tag_id}" - object does not exist."""
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data):
        return IotData.objects.create(**validated_data)

