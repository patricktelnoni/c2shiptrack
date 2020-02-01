from rest_framework import serializers
from c2shiptrack.models import *

class TacticalFiguresSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacticalFigures
        fields = '__all__'

class TacticalFigureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TacticalFigureList
        fields = '__all__'

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'

class ReplayTrackGeneralSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplayTrackGeneralSetting
        fields = '__all__'

class ReplaySystemTrackProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaySystemTrackProcessing
        fields = '__all__'

class ReplaySystemTrackMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaySystemTrackMission
        fields = '__all__'

class ReplaySystemTrackLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaySystemTrackLink
        fields = '__all__'

class ReplaySystemTrackKineticSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaySystemTrackKinetic
        fields = '__all__'



class ReplaySystemTrackIdentificationSerializer(serializers.Serializer):
    session = serializers.IntegerField()
    system_track_number = serializers.IntegerField()
    identity = serializers.CharField(max_length=255)
    environment = serializers.CharField(max_length=255)
    air_platform = serializers.CharField(max_length=255)
    surf_platform = serializers.CharField(max_length=255)
    land_platform = serializers.CharField(max_length=255)
    air_platform_activity = serializers.CharField(max_length=255)
    surf_platform_activity = serializers.CharField(max_length=255)
    land_platform_activity = serializers.CharField(max_length=255)
    air_specific = serializers.CharField(max_length=255)
    surf_specific = serializers.CharField(max_length=255)
    land_specific = serializers.CharField(max_length=255)
    created_time = serializers.DateTimeField()


class ReplaySystemTrackGeneralSerializer(serializers.Serializer):
    session = serializers.IntegerField()
    system_track_number = serializers.IntegerField()
    track_name = serializers.CharField()
    network_track_number = serializers.IntegerField()
    identity = serializers.CharField()
    environment = serializers.CharField()
    object_type = serializers.CharField()
    object_id = serializers.IntegerField()
    primitive_data_source = serializers.CharField()
    accuracy_level = serializers.IntegerField()
    source = serializers.CharField()
    own_unit_indicator = serializers.CharField()
    iu_indicator = serializers.CharField()
    c2_indicator = serializers.CharField()
    special_processing_indicator = serializers.CharField()
    force_tell_indicator = serializers.CharField()
    emergency_indicator = serializers.CharField()
    simulation_indicator = serializers.CharField()
    last_update_time = serializers.DateTimeField()
    initiation_time = serializers.DateTimeField()
    created_time = serializers.DateTimeField()
    class Meta:
        model = ReplaySystemTrackGeneral
        fields  = '__all__'

class ReplayReferencePointSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReplayReferencePoint
        fields  = '__all__'

class ReplayAisDataSerializer(serializers.Serializer):
    # system_track_number = serializers.IntegerField()
    # session = serializers.IntegerField()
    # mmsi_number = serializers.IntegerField()
    # name = serializers.CharField()
    # radio_call_sign = serializers.CharField()
    # imo_number = serializers.IntegerField()
    # navigation_status = serializers.CharField()
    # destination = serializers.CharField()
    # dimensions_of_ship = serializers.CharField()
    # type_of_ship_or_cargo = serializers.CharField()
    # rate_of_turn = serializers.FloatField()
    # position_accuracy = serializers.FloatField()
    # gross_tonnage = serializers.IntegerField()
    # ship_country = serializers.CharField()
    # created_time = serializers.DateTimeField()
    # eta_at_destination = serializers.DateTimeField()
    # vendor_id = serializers.CharField()


    class Meta:
        model   = ReplayAisData
        fields  = '__all__'


class ReferencePointsSerializer(serializers.ModelSerializer):
    session = serializers.IntegerField()
    object_type = serializers.CharField()
    object_id = serializers.IntegerField()
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    altitude = serializers.FloatField()
    visibility_type = serializers.CharField()
    point_amplification_type = serializers.CharField()
    is_editable = serializers.BooleanField()
    network_track_number = serializers.IntegerField()
    link_status_type = serializers.CharField()
    last_update_time = serializers.DateTimeField()

class AreaAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = AreaAlerts
        fields  = '__all__'


