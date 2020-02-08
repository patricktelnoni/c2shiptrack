import logging


from c2shiptrack.celery import app
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import task
from c2shiptrack.models import *
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
import channels.layers
from asgiref.sync import async_to_sync
import json
import channels
from celery import shared_task
import numpy as np
from datetime import timedelta

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@shared_task
def test(arg):
    print('world')

# @periodic_task(run_every=timedelta(seconds=10))
@periodic_task(run_every=timedelta(seconds=10))
def tes_kirim():
    channel_layer   = channels.layers.get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(

            'chat_queen',

            {
                'type': 'chat_message',
                'message': 'tolong dong ini kok error',
            })
    except:
        logging.exception('Problem sending %s' )




    return None

@periodic_task(run_every=timedelta(seconds=300))
def area_alert():
    sql = "SELECT s.id, aa.* " \
            "FROM area_alerts aa " \
            "JOIN sessions s ON aa.session_id=s.id " \
            "JOIN(" \
            "   SELECT session_id,object_id,max(last_update_time) last_update_time" \
            "   FROM area_alerts" \
            "   GROUP BY session_id,object_id" \
            ") mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time " \
            " and aa.session_id=mx.session_id " \
            "WHERE s.end_time is NULL " \
            "ORDER BY aa.object_id;"
    query = AreaAlerts.objects.raw(sql)
    serialized = []
    # query = ReferencePoints.objects.latest('last_update_time')[0]
    # query = ReferencePoints.objects.all()
    if 'aa_status' not in cache:
        for p in query:
            data = {
                'id' :p.id,
                'object_type' :p.object_type,
                'object_id' :p.object_id,
                'warning_type' :p.warning_type,
                'track_name' :p.track_name,
                'last_update_time' :str(p.last_update_time),
                'mmsi_number' :p.mmsi_number,
                'ship_name' :p.ship_name,
                'track_source_type' :p.track_source_type,
                'is_visible' :p.is_visible,

            }
            serialized.append(data)
        # print(serialized)
        cache.set('aa_status', 'CREATE', timeout=CACHE_TTL)
        cache.set('aa', serialized, timeout=CACHE_TTL)
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_queen',
            {
                'type': 'chat_message',
                'message': serialized

            },
        )

    if len(cache.get('aa')) != len(query):
        deleted = []
        for c in range(len(cache.get('aa'))):
            if cache.get('rp')[c]['session_id'] not in query[c].values():
                data = {
                    # 'session_id'        : cache.get('rp')[c]['object_id'],
                    # 'nama'              : cache.get('rp')[c]['ship_name'],
                    # 'last_update_time'  : str(cache.get('rp')[c]['last_update_time']),
                    # 'visibility_type'   : cache.get('rp')[c]['is_visible'],

                    'id': cache.get('rp')[c].id,
                    'object_type': cache.get('rp')[c].object_type,
                    'object_id': cache.get('rp')[c].object_id,
                    'warning_type': cache.get('rp')[c].warning_type,
                    'track_name': cache.get('rp')[c].track_name,
                    'last_update_time': str(cache.get('rp')[c].last_update_time),
                    'mmsi_number': cache.get('rp')[c].mmsi_number,
                    'ship_name': cache.get('rp')[c].ship_name,
                    'track_source_type': cache.get('rp')[c].track_source_type,
                    'is_visible': cache.get('rp')[c].is_visible,
                }
                deleted.append(data)
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : deleted
                    },
                )

    if 'aa_status' in cache and cache.get('rp_status') == 'CREATE':
        cached = cache.get('aa')
        # print("Panjang di cache : " +  len(cached)  + "Panjang dari query, "  + len(query))
        # print(query)
        # print(cached)

        for q in range(len(query)):
            if cached[q]['last_update_time'] != query[q].last_update_time:
                data = {
                    # 'session_id': query[q].object_id,
                    # 'ship_name': query[q].ship_name,
                    # 'last_update_time': str(query[q].last_update_time),
                    # 'visibility_type': query[q].is_visible,

                'id' :query[q].id,
                'object_type' :query[q].object_type,
                'object_id' :query[q].object_id,
                'warning_type' :query[q].warning_type,
                'track_name' :query[q].track_name,
                'last_update_time' :str(query[q].last_update_time),
                'mmsi_number' :query[q].mmsi_number,
                'ship_name' :query[q].ship_name,
                'track_source_type' :query[q].track_source_type,
                'is_visible' :query[q].is_visible,
                }
                # serialized.append(data)
                cached[q]       = data
                channel_layer   = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : cached
                    },
                )
        cache.set('aa_status', 'UPDATE', timeout=CACHE_TTL)
        cache.set('aa', serialized, timeout=CACHE_TTL)
    return None

# @periodic_task(run_every=crontab(minute=0))
@periodic_task(run_every=timedelta(seconds=300))
def reference_point():
    serialized = []
    # query = ReferencePoints.objects.latest('last_update_time')[0]
    query = ReferencePoints.objects.all()
    if 'rp_status' not in cache:
        for p in query:
            data = {
                'object_type': p.object_type,
                'object_id': p.object_id,
                'name': p.name,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'altitude': p.altitude,
                'visibility_type': p.visibility_type,
                'point_amplification_type': p.point_amplification_type,
                'is_editable': p.is_editable,
                'network_track_number': p.network_track_number,
                'link_status_type': p.link_status_type,
                'last_update_time': str(p.last_update_time),
            }
            serialized.append(data)
        # print(serialized)
        cache.set('rp_status', 'CREATE', timeout=CACHE_TTL)
        cache.set('rp', serialized, timeout=CACHE_TTL)
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_queen',
            {
                'type': 'chat_message',
                'message': serialized

            },
        )

    if len(cache.get('rp')) != len(query):
        deleted = []
        for c in range(len(cache.get('rp'))):
            if cache.get('rp')[c]['session_id'] not in query[c].items():
                data = {
                    'object_type': query[c].object_type,
                    'object_id': query[c].object_id,
                    'name': query[c].name,
                    'latitude': query[c].latitude,
                    'longitude': query[c].longitude,
                    'altitude': query[c].altitude,
                    'visibility_type': query[c].visibility_type,
                    'point_amplification_type': query[c].point_amplification_type,
                    'is_editable': query[c].is_editable,
                    'network_track_number': query[c].network_track_number,
                    'link_status_type': query[c].link_status_type,
                    'last_update_time': str(query[c].last_update_time),
                }
                deleted.append(data)
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : deleted
                    },
                )


    if 'rp_status' in cache and cache.get('rp_status') == 'CREATE':
        cached = cache.get('rp')
        for q in range(len(query)):
            if cached[q]['last_update_time'] != query[q].last_update_time :
                data = {
                    'object_type': query[q].object_type,
                    'object_id': query[q].object_id,
                    'name': query[q].name,
                    'latitude': query[q].latitude,
                    'longitude': query[q].longitude,
                    'altitude': query[q].altitude,
                    'visibility_type': query[q].visibility_type,
                    'point_amplification_type': query[q].point_amplification_type,
                    'is_editable': query[q].is_editable,
                    'network_track_number': query[q].network_track_number,
                    'link_status_type': query[q].link_status_type,
                    'last_update_time': str(query[q].last_update_time),
                }
                # serialized.append(data)
                cached[q] = data
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : cached
                    },
                )
        cache.set('rp_status', 'UPDATE', timeout=CACHE_TTL)
        cache.set('rp', serialized, timeout=CACHE_TTL)

    # if cache.get('rp') == 'UPDATE':
    #     print('update')
    # if 'rp' in cache:
    #     # get results from cache
    #     if 'rp_status' in cache:
    #         cache.set('rp_status', 'UPDATE', timeout=CACHE_TTL)
    #     results = cache.get('rp')
    #
    # else:
    #     serialized = []
    #     for p in query:
    #         data = {'session_id': p.object_id, 'nama': p.name}
    #         serialized.append(data)
    #     # store data in cache
    #     cache.set('rp', serialized, timeout=CACHE_TTL)
    #     cache.set('rp_status', 'CREATE', timeout=CACHE_TTL)
    #     results = serialized

    return None

# @periodic_task(run_every=crontab(minute="*"))
@periodic_task(run_every=timedelta(seconds=300))
def tactical_list():
    query = TacticalFigureList.objects.all()
    serialized = []
    if 'tl_status' not in cache:
        for p in query:
            data = {
                'object_id' :p.object_id,
                'object_type' :p.object_type,
                'name' :p.name,
                'environment' :p.environment,
                'shape' :p.shape,
                'displaying_popup_alert_status' :p.displaying_popup_alert_status,
                'line_color' :p.line_color,
                'fill_color' :p.fill_color,
                'identity_list' :p.identity_list,
                'warning_list' :p.warning_list,
                'evaluation_type' :p.evaluation_type,
                'visibility_type' :p.visibility_type,
                'last_update_time' :str(p.last_update_time),
                'network_track_number' :p.network_track_number,
                'link_status_type' :p.link_status_type,
                'is_editable' :p.is_editable,
                'point_amplification_type' :p.point_amplification_type,
                'point_keys' :p.point_keys,
                'points' :p.points

            }
            serialized.append(data)
        # print(serialized)
        cache.set('tl_status', 'CREATE', timeout=CACHE_TTL)
        cache.set('tl', serialized, timeout=CACHE_TTL)
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_queen',
            {
                'type': 'chat_message',
                'message': serialized,
            },
        )

    if len(cache.get('tl')) != len(query):
        deleted = []
        for c in range(len(cache.get('tl'))):
            if cache.get('tl')[c]['session_id'] not in query[c].values():
                data = {
                    'object_id': query[c].object_id,
                    'object_type': query[c].object_type,
                    'name': query[c].name,
                    'environment': query[c].environment,
                    'shape': query[c].shape,
                    'displaying_popup_alert_status': query[c].displaying_popup_alert_status,
                    'line_color': query[c].line_color,
                    'fill_color': query[c].fill_color,
                    'identity_list': query[c].identity_list,
                    'warning_list': query[c].warning_list,
                    'evaluation_type': query[c].evaluation_type,
                    'visibility_type': query[c].visibility_type,
                    'last_update_time': str(query[c].last_update_time),
                    'network_track_number': query[c].network_track_number,
                    'link_status_type': query[c].link_status_type,
                    'is_editable': query[c].is_editable,
                    'point_amplification_type': query[c].point_amplification_type,
                    'point_keys': query[c].point_keys,
                    'points': query[c].points
                }
                deleted.append(data)
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : deleted
                    },
                )

    if 'tl_status' in cache and cache.get('tl_status') == 'CREATE':
        cached = cache.get('tl')
        # print("Panjang di cache : " +  len(cached)  + "Panjang dari query, "  + len(query))
        # print(query)
        # print(cached)

        for q in range(len(query)):
            if cached[q]['last_update_time'] != query[q].last_update_time:
                data = {
                    # 'session_id': query[q].object_id,
                    # 'nama': query[q].name,
                    # 'last_update_time': str(query[q].last_update_time),
                    # 'visibility_type': query[q].visibility_type,

                    'object_id': query[q].object_id,
                    'object_type': query[q].object_type,
                    'name': query[q].name,
                    'environment': query[q].environment,
                    'shape': query[q].shape,
                    'displaying_popup_alert_status': query[q].displaying_popup_alert_status,
                    'line_color': query[q].line_color,
                    'fill_color': query[q].fill_color,
                    'identity_list': query[q].identity_list,
                    'warning_list': query[q].warning_list,
                    'evaluation_type': query[q].evaluation_type,
                    'visibility_type': query[q].visibility_type,
                    'last_update_time': str(query[q].last_update_time),
                    'network_track_number': query[q].network_track_number,
                    'link_status_type': query[q].link_status_type,
                    'is_editable': query[q].is_editable,
                    'point_amplification_type': query[q].point_amplification_type,
                    'point_keys': query[q].point_keys,
                    'points': query[q].points
                }
                # serialized.append(data)
                cached[q] = data
                channel_layer = channels.layers.get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'chat_queen',
                    {
                        'type': 'chat_message',
                        'message' : cached
                    },
                )
        cache.set('tl_status', 'UPDATE', timeout=CACHE_TTL)
        cache.set('tl', serialized, timeout=CACHE_TTL)

    return None

# @periodic_task(run_every=crontab(minute="*"))
# def kirim_channel():
#     r = requests.get('http://127.0.0.1:8000/api/realtime_track/')
#     r.json()
#
#     # reverse_url = "https://127.0.0.1:8000/api/realtime_track"
#     # urllib.urlopen(reverse_url)
#     channel_layer = channels.layers.get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'chat_queen',
#         {
#             'type': 'chat_message',
#             'message': 'Ini dari task'
#         },
#     )
#     # return_5
#     return None
# kirim_channel.apply_async()
@task()
def test_task():
    ar_mandatory_table = ['replay_system_track_general',
                          'replay_system_track_kinetic',
                          'replay_system_track_processing',
                          'replay_track_general_setting']
    ar_mandatory_table_8 = ['replay_system_track_general',
                            'replay_system_track_kinetic',
                            'replay_system_track_processing',
                            'replay_system_track_identification',
                            'replay_system_track_link',
                            'replay_system_track_mission',
                            'replay_track_general_setting',
                            'replay_ais_data']
    ar_dis_track_number_mandatory_table = [[], [], [], []]
    ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
    last_system_track_number_kirim_datetime = ['0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                               '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                               '0000-00-00 00:00:00', '0000-00-00 00:00:00']


    mandatory_table = ar_mandatory_table

    for table in range(len(mandatory_table)):
        results = []
        if table not in cache:
            cache.set(table, 'kosongan', timeout=CACHE_TTL)
            exist = 0

        if ('replay_system_track_general' in cache and
                'replay_system_track_kinetic' in cache and
                'replay_system_track_processing' in cache and
                'replay_track_general_setting' in cache):
            results = cache.get(table)
            exist = 1
            # return Response(results, status=status.HTTP_201_CREATED)

        if (table == 'replay_system_track_general'):
            query = "SELECT s.id as id, st.* " \
                    "FROM " + ar_mandatory_table[table] + " st " \
                                                               "JOIN sessions s ON st.session_id=s.id JOIN (" \
                                                               "   SELECT session_id,system_track_number,max(created_time) created_time " \
                                                               "   FROM replay_system_track_general " \
                                                               "   GROUP BY session_id,system_track_number" \
                                                               ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
                                                               "WHERE s.end_time is NULL and st.own_unit_indicator='FALSE' " \
                                                               "ORDER BY st.system_track_number"
        else:
            query = "SELECT s.id as id, st.* " \
                    "FROM " + ar_mandatory_table[table] + " st " \
                                                               "JOIN sessions s ON st.session_id=s.id JOIN (" \
                                                               "   SELECT session_id,system_track_number,max(created_time) created_time " \
                                                               "   FROM replay_system_track_general " \
                                                               "   GROUP BY session_id,system_track_number" \
                                                               ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
                                                               "WHERE s.end_time is NULL " \
                                                               "ORDER BY st.system_track_number"
        # print(query)

        hasil = ReplaySystemTrackGeneral.objects.raw(query)
        session_id = 0
        system_track_number = 0
        # print(ar_mandatory_table[table])
        for p in hasil:
            # print(p[0])
            ar_dis_track_number_mandatory_table[table].append(p.system_track_number)
            session_id = p.id
            system_track_number = p.system_track_number

        exist = 1

        if (exist == 1):
            ar_temp = list(ar_dis_track_number_mandatory_table[0])
            ar_temp.sort(reverse=True)
            # array yang pertama adalah id terakhir
            columns = (
                'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name',
                'iu_indicator',
                'airborne_indicator')

            for ix in range(len(ar_mandatory_table_8)):
                q = "SELECT s.id, max(r.created_time) created_time FROM " + ar_mandatory_table_8[ix];
                q = q + " r JOIN sessions s ON s.id = r.session_id WHERE r.session_id = " + str(session_id) + \
                    " AND system_track_number = " + str(
                    system_track_number) + "GROUP BY created_time, s.id";

                created_time = ''
                for row in ReplaySystemTrackProcessing.objects.raw(q):
                    created_time = str(row.created_time)
                # dapatkan created time yang terakhir per 8 tabel tersebut
                q = "SELECT max(created_time) created_time FROM " + ar_mandatory_table_8[ix];
                q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(
                    system_track_number);
                if (created_time > str(last_system_track_number_kirim_datetime[ix])):
                    # kirimkan data dengan created time terbaru
                    # dan simpan ke last_system_track_number_kirim
                    last_system_track_number_kirim_datetime[ix] = created_time
                print(session_id)
                if (ar_mandatory_table_8[ix] == 'replay_system_track_general'):
                    q = "SELECT s.id, source FROM replay_system_track_general r " \
                        " JOIN sessions s on r.session_id=s.id " \
                        "WHERE r.session_id = " + str(
                        session_id) + " AND r.system_track_number = " + str(system_track_number);
                    if last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
                        q = q + " AND r.created_time = null"
                    else:
                        q = q + " AND r.created_time = '" + last_system_track_number_kirim_datetime[
                            ix] + "'"

                    for data_source in ReplaySystemTrackGeneral.objects.raw(q):
                        if data_source.source == 'AIS_TYPE':
                            query = "SELECT s.id, r.system_track_number,r.created_time,identity,environment,source,track_name,iu_indicator" \
                                    "FROM ";
                            query = query + ar_mandatory_table_8[
                                ix] + " r join sessions s on s.id = r.session_id " \
                                      "LEFT OUTER JOIN replay_ais_data b on r.system_track_number = b.system_track_number " \
                                      "WHERE r.session_id = " + str(
                                session_id) + " AND r.system_track_number = " + str(system_track_number)
                            if last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
                                query = query + " AND r.created_time = null"
                            else:
                                query = query + " AND r.created_time = '" + \
                                        last_system_track_number_kirim_datetime[
                                            ix] + "'"
                            print(query)
                        else:
                            query = "SELECT s.id, system_track_number,created_time,identity,environment,source,track_name,iu_indicator  FROM ";
                            query = query + ar_mandatory_table_8[
                                ix] + " r join sessions s on s.id = r.session_id WHERE session_id = " + str(
                                session_id) + " AND system_track_number = " + str(system_track_number);
                            if last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
                                query = query + " AND created_time = null"
                            else:
                                query = query + " AND created_time = '" + last_system_track_number_kirim_datetime[
                                    ix] + "'"

                        for row in Sessions.objects.raw(query):
                            data = []
                            data.append(row.system_track_number)
                            data.append(row.created_time)
                            data.append(row.identity)
                            data.append(row.environment)
                            data.append(row.source)
                            data.append(row.track_name)
                            data.append(row.iu_indicator)

                            # print(row)
                        results.append(dict(zip(columns, data)))
                    # hasil = json.dumps(results, indent=2, default=str)
                    # return Response(results, status=status.HTTP_201_CREATED)

                if (ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
                    q = "SELECT a.session_id as id, latitude,longitude,speed_over_ground,course_over_ground, " \
                        "b.name as ship_name, b.type_of_ship_or_cargo as type_of_ship, c.source  FROM ";
                    q = q + ar_mandatory_table_8[
                        ix] + " a LEFT OUTER JOIN replay_ais_data b ON a.system_track_number = b.system_track_number " \
                              "LEFT OUTER JOIN replay_system_track_general c on a.system_track_number = c.system_track_number " \
                              " WHERE a.session_id = " + str(
                        session_id) + " AND a.system_track_number = " + str(system_track_number);
                    q = q + " AND a.created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";

                    for row in ReplaySystemTrackKinetic.objects.raw(q):
                        results[len(results) - 1]['latitude'] = row.latitude
                        results[len(results) - 1]['longitude'] = row.longitude
                        results[len(results) - 1]['speed_over_ground'] = row.speed_over_ground
                        results[len(results) - 1]['course_over_ground'] = row.course_over_ground
                        results[len(results) - 1]['ship_name'] = row.ship_name
                        results[len(results) - 1]['type_of_ship'] = row.type_of_ship
                        results[len(results) - 1]['source'] = row.source

                    # hasil = json.dumps(results, indent=2, default=str)


                if (ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
                    q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
                    q = q + ar_mandatory_table_8[
                        ix] + " LEFT OUTER JOIN replay_system_track_general ON WHERE session_id = " + str(
                        session_id) + " AND system_track_number = " + str(system_track_number);
                    q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    print(q)

                    for row in ReplaySystemTrackProcessing.objects.raw(q):
                        results[len(results) - 1]['track_join_status'] = row.rack_join_status
                        results[len(results) - 1]['track_fusion_status'] = row.track_fusion_status
                        results[len(results) - 1]['track_phase'] = row.track_phase

                    # hasil = json.dumps(results, indent=2, default=str)
                    # return Response(results, status=status.HTTP_201_CREATED)

                if (ar_mandatory_table_8[ix] == 'replay_ais_data'):
                    icek_ais = 0
                    if (last_system_track_number_kirim_datetime[ix] != 'None'):
                        q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                        q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";

                        for row in ReplayAisData.objects.raw(q):
                            results[len(results) - 1]['type_of_ship_or_cargo'] = row.type_of_ship_or_cargo
                            results[len(results) - 1]['ship_name'] = row.ship_name
                            icek_ais = 1

                    else:
                        q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                        q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        q = q + " ORDER BY created_time DESC ) aa LIMIT 1";

                        for row in Sessions.objects.raw(q):
                            results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
                            results[len(results) - 1]['ship_name'] = row[1]
                            icek_ais = 1

                    if (icek_ais == 0):
                        results[len(results) - 1]['type_of_ship_or_cargo'] = '-'
                        results[len(results) - 1]['ship_name'] = '-'
                    print(q)
                    # hasil = json.dumps(results, indent=2, default=str)
                    # return Response(results, status=status.HTTP_201_CREATED)

                if (ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
                    q = "SELECT track_visibility FROM ";
                    q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                        session_id) + " AND system_track_number = " + str(system_track_number);
                    q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";

                    for row in ReplayTrackGeneralSetting.objects.raw(q):
                        results[len(results) - 1]['track_visibility'] = row[0]
        # store data in cache

        # cache.set('rstp', serialized, timeout=CACHE_TTL)
    # return Response(serialized, status=status.HTTP_201_CREATED)
    channel_layer = channels.layers.get_channel_layer()
    # Send message to WebSocket
    async_to_sync(channel_layer.send)(text_data=json.dumps(
        results
    ))

    return None


# @app.task
# def send_verification_email(user_id):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=user_id)
#         send_mail(
#             'Verify your QuickPublisher account',
#             'Follow this link to verify your account: '
#             'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
#             'from@quickpublisher.dev',
#             [user.email],
#             fail_silently=False,
#         )
#     except UserModel.DoesNotExist:
#         logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)