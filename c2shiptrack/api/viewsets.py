from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from c2shiptrack.unusedmodels import *
from .serializer import *

class ReferencePointsViewSet(viewsets.ModelViewSet):
    # queryset = ReferencePoints.objects.all()

    serializer_class = ReferencePointsSerializer
    model = ReferencePoints

    def list(self, request, *args, **kwargs):
        # serialized      = serializer(queryset, many=True)
        # print(serialized.data[2].get('name'))
        query = 'SELECT session_id as id, * FROM reference_point'
        serialized = []
        for p in ReplayAisData.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.name}
            serialized.append(data)
        return Response(serialized)

class ReplayAisDataViewSet(viewsets.ModelViewSet):
    # queryset = ReplayAisData.objects.all()
    # queryset = ReplayAisData.objects.filter('imo_number')
    model               = ReplayAisData
    serializer_class    = ReplayAisDataSerializer
    queryset            = ReplayAisData.objects.raw('SELECT session_id as id, * FROM replay_ais_data')


    def list(self, request, *args, **kwargs):
        # serialized      = serializer(queryset, many=True)
        # print(serialized.data[2].get('name'))
        query = 'SELECT session_id as id, * FROM replay_ais_data'
        serialized = []
        for p in ReplayAisData.objects.raw(query):
            data = {'session_id': p.id, 'nama' : p.name}
            serialized.append(data)
        return Response(serialized)
        # return ReplayAisData.object.raw("SELECT * FROM replay_ais_data")

class ReplayReferencePointViewSet(viewsets.ModelViewSet):
    # queryset = ReplayReferencePoint.objects.all()
    serializer_class = ReplayReferencePointSerializer
    model = ReplayReferencePoint
    queryset = ReplayReferencePoint.objects.raw('SELECT session_id as id, * FROM replay_reference_point')

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_reference_point'
        serialized = []
        for p in ReplayReferencePoint.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.name}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackGeneralViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackGeneral.objects.raw('SELECT session_id as id, track_name FROM replay_system_track_general')
    serializer_class = ReplaySystemTrackGeneralSerializer
    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_system_track_general'
        serialized = []
        for p in ReplaySystemTrackGeneral.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackIdentificationViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackIdentification.objects.all()
    # serializer_class = ReplaySystemTrackIdentificationSerializer
    queryset = ReplaySystemTrackIdentification.objects.raw(
        'SELECT session_id as id, * FROM replay_system_track_identification')
    serializer_class = ReplaySystemTrackIdentificationSerializer

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_system_track_general'
        serialized = []
        for p in ReplaySystemTrackIdentification.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.system_track_number}
            serialized.append(data)
        return Response(serialized)
    # def list(self, request):
    #     # queryset = ReplaySystemTrackIdentification.objects.raw('SELECT * FROM replay_system_track_identification')
    #     # serializer = ReplaySystemTrackIdentification(queryset, many=True)
    #     serializer = ReplaySystemTrackIdentificationSerializer(
    #         instance=ReplaySystemTrackIdentification.values(), many=True)
    #     return Response(serializer.data)


class ReplaySystemTrackKineticViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackKinetic.objects.all()
    # serializer_class = ReplaySystemTrackKineticSerializer
    queryset = ReplaySystemTrackKinetic.objects.raw(
        'SELECT session_id as id, track_name FROM replay_system_track_kinetic')
    serializer_class = ReplaySystemTrackKineticSerializer

    def list(self, request):
        query = 'SELECT session_id as id, track_name FROM replay_system_track_kinetic'
        serialized = []
        for p in ReplaySystemTrackKinetic.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackLinkViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackLink.objects.all()
    # serializer_class = ReplaySystemTrackLinkSerializer
    queryset = ReplaySystemTrackLink.objects.raw(
        'SELECT session_id as id, track_name FROM replay_system_track_link')
    serializer_class = ReplaySystemTrackLinkSerializer

    def list(self, request):
        query = 'SELECT session_id as id, track_name FROM replay_system_track_link'
        serialized = []
        for p in ReplaySystemTrackLink.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackMissionViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackMission.objects.all()
    # serializer_class = ReplaySystemTrackMissionSerializer
    queryset = ReplaySystemTrackMission.objects.raw(
        'SELECT session_id as id, track_name FROM replay_system_track_mission')
    serializer_class = ReplaySystemTrackMissionSerializer

    def list(self, request):
        query = 'SELECT session_id as id, track_name FROM replay_system_track_mission'
        serialized = []
        for p in ReplaySystemTrackMission.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackProcessingViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackProcessing.objects.all()
    # serializer_class = ReplaySystemTrackProcessingSerializer
    queryset = ReplaySystemTrackProcessing.objects.raw(
        'SELECT session_id as id, track_name FROM replay_system_track_general')
    serializer_class = ReplaySystemTrackProcessingSerializer

    def list(self, request):
        query = 'SELECT session_id as id, track_name FROM replay_system_track_general'
        serialized = []
        for p in ReplaySystemTrackProcessing.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class ReplayTrackGeneralSettingViewSet(viewsets.ModelViewSet):
    # queryset = ReplayTrackGeneralSetting.objects.all()
    # serializer_class = ReplayTrackGeneralSettingSerializer
    queryset = ReplayTrackGeneralSetting.objects.raw(
        'SELECT session_id as id, track_name FROM replay_track_general_setting')
    serializer_class = ReplayTrackGeneralSettingSerializer

    def list(self, request):
        query = 'SELECT session_id as id, track_name FROM replay_track_general_setting'
        serialized = []
        for p in ReplayTrackGeneralSetting.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.track_name}
            serialized.append(data)
        return Response(serialized)

class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer

class TacticalFigureListViewSet(viewsets.ModelViewSet):
    queryset = TacticalFigureList.objects.all()
    serializer_class = TacticalFigureListSerializer

class TacticalFiguresViewSet(viewsets.ModelViewSet):
    queryset = TacticalFigures.objects.all()
    serializer_class = TacticalFiguresSerializer

class AreaAlertViewSet(viewsets.ModelViewSet):
    queryset = AreaAlerts.objects.all()
    serializer_class = AreaAlertsSerializer

