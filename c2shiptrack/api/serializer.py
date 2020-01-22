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



class ReplaySystemTrackIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReplaySystemTrackIdentification
        fields  = '__all__'

class ReplaySystemTrackGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReplaySystemTrackGeneral
        fields  = '__all__'

class ReplayReferencePointSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReplayReferencePoint
        fields  = '__all__'

class ReplayAisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReplayAisData
        fields  = '__all__'

class ReferencePointsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = ReferencePoints
        fields  = '__all__'

class AreaAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = AreaAlerts
        fields  = '__all__'


