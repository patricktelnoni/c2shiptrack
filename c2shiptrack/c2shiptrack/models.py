# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AreaAlerts(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    warning_type = models.CharField(max_length=255, blank=True, null=True)
    track_name = models.CharField(max_length=255, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    mmsi_number = models.IntegerField(blank=True, null=True)
    ship_name = models.CharField(max_length=100, blank=True, null=True)
    track_source_type = models.CharField(max_length=100, blank=True, null=True)
    is_visible = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_alerts'


class ReferencePoints(models.Model):
    object_type = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    visibility_type = models.CharField(max_length=100, blank=True, null=True)
    point_amplification_type = models.CharField(max_length=100, blank=True, null=True)
    is_editable = models.BooleanField(blank=True, null=True)
    network_track_number = models.IntegerField(blank=True, null=True)
    link_status_type = models.CharField(max_length=100, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reference_points'


class ReplayAisData(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    mmsi_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    radio_call_sign = models.CharField(max_length=255, blank=True, null=True)
    imo_number = models.IntegerField(blank=True, null=True)
    navigation_status = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    dimensions_of_ship = models.CharField(max_length=255, blank=True, null=True)
    type_of_ship_or_cargo = models.CharField(max_length=255, blank=True, null=True)
    rate_of_turn = models.FloatField(blank=True, null=True)
    position_accuracy = models.FloatField(blank=True, null=True)
    gross_tonnage = models.IntegerField(blank=True, null=True)
    ship_country = models.CharField(max_length=100, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    eta_at_destination = models.DateTimeField(blank=True, null=True)
    vendor_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_ais_data'


class ReplayReferencePoint(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    object_type = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    visibility_type = models.CharField(max_length=100, blank=True, null=True)
    point_amplification_type = models.CharField(max_length=100, blank=True, null=True)
    is_editable = models.BooleanField(blank=True, null=True)
    network_track_number = models.IntegerField(blank=True, null=True)
    link_status_type = models.CharField(max_length=100, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_reference_point'


class ReplaySystemTrackGeneral(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    track_name = models.CharField(max_length=255, blank=True, null=True)
    network_track_number = models.IntegerField(blank=True, null=True)
    identity = models.CharField(max_length=255, blank=True, null=True)
    environment = models.CharField(max_length=255, blank=True, null=True)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    primitive_data_source = models.CharField(max_length=2, blank=True, null=True)
    accuracy_level = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    own_unit_indicator = models.CharField(max_length=20, blank=True, null=True)
    iu_indicator = models.CharField(max_length=20, blank=True, null=True)
    c2_indicator = models.CharField(max_length=20, blank=True, null=True)
    special_processing_indicator = models.CharField(max_length=20, blank=True, null=True)
    force_tell_indicator = models.CharField(max_length=20, blank=True, null=True)
    emergency_indicator = models.CharField(max_length=20, blank=True, null=True)
    simulation_indicator = models.CharField(max_length=20, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    initiation_time = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_general'


class ReplaySystemTrackIdentification(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    identity = models.CharField(max_length=255, blank=True, null=True)
    environment = models.CharField(max_length=255, blank=True, null=True)
    air_platform = models.CharField(max_length=255, blank=True, null=True)
    surf_platform = models.CharField(max_length=255, blank=True, null=True)
    land_platform = models.CharField(max_length=255, blank=True, null=True)
    air_platform_activity = models.CharField(max_length=255, blank=True, null=True)
    surf_platform_activity = models.CharField(max_length=255, blank=True, null=True)
    land_platform_activity = models.CharField(max_length=255, blank=True, null=True)
    air_specific = models.CharField(max_length=255, blank=True, null=True)
    surf_specific = models.CharField(max_length=255, blank=True, null=True)
    land_specific = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_identification'


class ReplaySystemTrackKinetic(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    track_name = models.CharField(max_length=255, blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    range = models.FloatField(blank=True, null=True)
    bearing = models.FloatField(blank=True, null=True)
    height_depth = models.FloatField(blank=True, null=True)
    speed_over_ground = models.FloatField(blank=True, null=True)
    course_over_ground = models.FloatField(blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_kinetic'


class ReplaySystemTrackLink(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    network_track_number = models.IntegerField(blank=True, null=True)
    associated_track_number = models.IntegerField(blank=True, null=True)
    originator_address = models.IntegerField(blank=True, null=True)
    controlling_unit_address = models.IntegerField(blank=True, null=True)
    network_track_quality = models.IntegerField(blank=True, null=True)
    link_status = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_link'


class ReplaySystemTrackMission(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    mission_name = models.CharField(max_length=255)
    route = models.CharField(max_length=255, blank=True, null=True)
    voice_call_sign = models.CharField(max_length=255, blank=True, null=True)
    voice_frequency_channel = models.IntegerField(blank=True, null=True)
    fuel_status = models.IntegerField(blank=True, null=True)
    radar_coverage = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_mission'


class ReplaySystemTrackProcessing(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    track_fusion_status = models.CharField(max_length=255, blank=True, null=True)
    track_join_status = models.CharField(max_length=255, blank=True, null=True)
    daughter_tracks = models.TextField(blank=True, null=True)  # This field type is a guess.
    track_phase_type = models.CharField(max_length=255, blank=True, null=True)
    track_suspect_level = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_system_track_processing'


class ReplayTrackGeneralSetting(models.Model):
    session = models.ForeignKey('Sessions', models.DO_NOTHING)
    system_track_number = models.IntegerField()
    speed_label_visibility = models.CharField(max_length=255, blank=True, null=True)
    track_name_label_visibility = models.CharField(max_length=255, blank=True, null=True)
    radar_coverage_visibility = models.CharField(max_length=255, blank=True, null=True)
    track_visibility = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'replay_track_general_setting'


class Sessions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class TacticalFigureList(models.Model):
    object_id = models.IntegerField(primary_key=True)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    environment = models.CharField(max_length=255, blank=True, null=True)
    shape = models.CharField(max_length=255, blank=True, null=True)
    displaying_popup_alert_status = models.BooleanField(blank=True, null=True)
    line_color = models.TextField(blank=True, null=True)  # This field type is a guess.
    fill_color = models.TextField(blank=True, null=True)  # This field type is a guess.
    identity_list = models.TextField(blank=True, null=True)  # This field type is a guess.
    warning_list = models.TextField(blank=True, null=True)  # This field type is a guess.
    evaluation_type = models.CharField(max_length=255, blank=True, null=True)
    visibility_type = models.CharField(max_length=255, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    network_track_number = models.IntegerField(blank=True, null=True)
    link_status_type = models.CharField(max_length=100, blank=True, null=True)
    is_editable = models.BooleanField(blank=True, null=True)
    point_amplification_type = models.CharField(max_length=100, blank=True, null=True)
    point_keys = models.TextField(blank=True, null=True)  # This field type is a guess.
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tactical_figure_list'


class TacticalFigures(models.Model):
    session = models.ForeignKey(Sessions, models.DO_NOTHING)
    object_type = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    tf_name = models.CharField(max_length=255, blank=True, null=True)
    tf_environment = models.CharField(max_length=255, blank=True, null=True)
    tf_shape = models.CharField(max_length=255, blank=True, null=True)
    tf_line_color = models.TextField(blank=True, null=True)  # This field type is a guess.
    tf_fill_color = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_visible = models.CharField(max_length=255, blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    network_track_number = models.IntegerField(blank=True, null=True)
    link_status_type = models.CharField(max_length=100, blank=True, null=True)
    is_editable = models.BooleanField(blank=True, null=True)
    point_amplification_type = models.CharField(max_length=100, blank=True, null=True)
    point_keys = models.TextField(blank=True, null=True)  # This field type is a guess.
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tactical_figures'
