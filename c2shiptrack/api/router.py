from rest_framework import routers

from .viewsets import *


router = routers.SimpleRouter()

router.register(r'login', LoginViewset, basename='login')
router.register(r'lokasi', LokasiViewset, basename='lokasi')
router.register(r'session', SessionViewset, basename='session')
router.register(r'stored_replay', StoredReplayViewset, basename='stored_replay')
# router.register(r'list_user', UserViewset, basename='list_user')

urlpatterns = router.urls

# router.register(r'replay_ais_data', ReplayAisDataViewSet, basename='replay_ais_data')
# router.register(r'replay_reference_point', ReplayReferencePointViewSet, basename='replay_reference_point')
# router.register(r'replay_system_track_general', ReplaySystemTrackGeneralViewSet)
# router.register(r'replay_system_track_identification', ReplaySystemTrackIdentificationViewSet)
# router.register(r'replay_system_track_kinetic', ReplaySystemTrackKineticViewSet)
# router.register(r'replay_system_track_link', ReplaySystemTrackLinkViewSet)
# router.register(r'replay_system_track_mission', ReplaySystemTrackMissionViewSet)
# router.register(r'replay_system_track_processing', ReplaySystemTrackProcessingViewSet)
# router.register(r'replay_track_general_setting', ReplayTrackGeneralSettingViewSet)
# router.register(r'sessions', SessionsViewSet)
# router.register(r'realtime_track', GetRealtimeTrackViewSet)
# router.register(r'replay_track', ReplayTrackViewSet)
# router.register(r'tactical_figure_list', TacticalFigureListViewSet)
# router.register(r'tactical_figures', TacticalFiguresViewSet)
# router.register(r'area_alert', AreaAlertViewSet)
# router.register(r'^test_mentah', ListCreateAPIView.as_view(queryset='SELECT session_id as id, name FROM replay_ais_data', serializer_class=ReplayAisDataSerializer), basename='user-list')
# router.register(r'get_location', LocationViewSet, basename='locations')
#
# urlpatterns = router.urls
# router.register(r'get_location/<float:langitude>/<float:longitude>/$',
#                 LocationViewSet, basename='locations')