from rest_framework import serializers
from api.models import Devices, Tags, ValueTypes, IotData
from distutils.util import strtobool


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('device_id', 'name', 'description', 'type')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag_id', 'name', 'description', 'device', 'value_type')

    #def validate(self, data):
    #    if 'bob' not in data['tag_id'].lower():
    #        raise serializers.ValidationError("Bob not in tag ID")
    #    return data


class ValTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueTypes
        fields = ('value_type_id', 'name', 'type')


class IotTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotData
        fields = ('tag','value_text')


class IotIntegerSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotData
        fields = ('tag','value_int')


class IotDecimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotData
        fields = ('tag','value_dec')


class IotBooleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = IotData
        fields = ('tag','value_bool')


class TagDataSerializer(serializers.ModelSerializer):
    value = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = IotData
        fields = ('tag','value','value_text','value_int','value_dec','value_bool')

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        tag_type = Tags.objects.select_related('value_type').get(pk=data['tag']).value_type.type
        val = str(data['value'])

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


    def create(self, validated_data):
        return IotData.objects.create(**validated_data)

