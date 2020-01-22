from rest_framework import routers, serializers, viewsets
from c2shiptrack.unusedmodels import *
from .serializer import *

class ReferencePointsViewSet(viewsets.ModelViewSet):
    queryset = ReferencePoints.objects.all()
    serializer_class = ReferencePointsSerializer

class ReplayAisDataViewSet(viewsets.ModelViewSet):
    queryset = ReplayAisData.objects.all()
    serializer_class = ReplayAisDataSerializer

class ReplayReferencePointViewSet(viewsets.ModelViewSet):
    queryset = ReplayReferencePoint.objects.all()
    serializer_class = ReplayReferencePointSerializer

class ReplaySystemTrackGeneralViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackGeneral.objects.all()
    serializer_class = ReplaySystemTrackGeneralSerializer

class ReplaySystemTrackIdentificationViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackIdentification.objects.all()
    serializer_class = ReplaySystemTrackIdentificationSerializer

class ReplaySystemTrackKineticViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackKinetic.objects.all()
    serializer_class = ReplaySystemTrackKineticSerializer

class ReplaySystemTrackLinkViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackLink.objects.all()
    serializer_class = ReplaySystemTrackLinkSerializer

class ReplaySystemTrackMissionViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackMission.objects.all()
    serializer_class = ReplaySystemTrackMissionSerializer

class ReplaySystemTrackProcessingViewSet(viewsets.ModelViewSet):
    queryset = ReplaySystemTrackProcessing.objects.all()
    serializer_class = ReplaySystemTrackProcessingSerializer

class ReplayTrackGeneralSettingViewSet(viewsets.ModelViewSet):
    queryset = ReplayTrackGeneralSetting.objects.all()
    serializer_class = ReplayTrackGeneralSettingSerializer

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

