from rest_framework import routers
from .viewsets import *

router = routers.SimpleRouter()

router.register(r'reference_points', ReferencePointsViewSet)
router.register(r'replay_ais_data', ReplayAisDataViewSet)
router.register(r'replay_reference_point', ReplayReferencePointViewSet)
router.register(r'replay_system_track_general', ReplaySystemTrackGeneralViewSet)
router.register(r'replay_system_track_identification', ReplaySystemTrackIdentificationViewSet)
router.register(r'replay_system_track_kinetic', ReplaySystemTrackKineticViewSet)
router.register(r'replay_system_track_link', ReplaySystemTrackLinkViewSet)
router.register(r'replay_system_track_mission', ReplaySystemTrackMissionViewSet)
router.register(r'replay_system_track_processing', ReplaySystemTrackProcessingViewSet)
router.register(r'replay_track_general_setting', ReplayTrackGeneralSettingViewSet)
router.register(r'sessions', SessionsViewSet)
router.register(r'tactical_figure_list', TacticalFigureListViewSet)
router.register(r'tactical_figures', TacticalFiguresViewSet)
router.register(r'area_alert', AreaAlertViewSet)
# router.register(r'get_location', LocationViewSet, basename='locations')
#
# urlpatterns = router.urls
# router.register(r'get_location/<float:langitude>/<float:longitude>/$',
#                 LocationViewSet, basename='locations')