from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from .serializer import *
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.models import User
from c2shiptrack.models import *
import json
from rest_framework.decorators import api_view, renderer_classes
from django.http import JsonResponse

from django.db import connection
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import channels
# from datetime import timedelta, datetime
# import datetime as dt

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
UPDATE_RATE = 10

class SessionViewset(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer

class LokasiViewset(viewsets.ModelViewSet):
    queryset = Lokasi.objects.all()
    serializer_class = LokasiSerializer

class StoredReplayViewset(viewsets.ModelViewSet):
    queryset = StoredReplay.objects.all()
    serializer_class = StoredReplaySerializer

# class UserViewset(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer
#     @api_view()
#     def list(self, request):
#         queryset = User.objects.select_related('lokasi_user').all()
#         return Response(LoginSerializer(queryset, many=True).data)

class LoginViewset(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @api_view()
    def login_by_email(self, username, password):
        queryset = User.objects.filter(username=username)
        return Response(LoginSerializer(queryset, many=True).data)

    @api_view()
    def list_user(request):
        queryset = LokasiUser.objects.select_related('user').select_related('lokasi').all()
        return Response(UserJoinedSerializer(queryset, many=True).data)

    @api_view()
    def detail_user(request, user_id):
        queryset = LokasiUser.objects.select_related('user').select_related('lokasi').filter(user=user_id)
        return Response(UserJoinedSerializer(queryset, many=True).data)

    @csrf_protect
    def update_user(request, user_id):
        post_data = json.loads(request.body)
        user = {
            "username": post_data['user']['username'],
            "password": post_data['user']['password'],

        }
        sqlUser = "UPDATE auth_user " \
              "set username = '" + post_data['user']['username'] + "' , " \
                "password = '" + post_data['user']['password'] + "' WHERE id = '" + str(user_id[0]) + "' "
        print(sqlUser)
        cursor = connection.cursor()
        cursor.execute(sqlUser)
        connection.commit()


        sqlLokasiUser = "UPDATE c2shiptrack_lokasiuser " \
                  "set lokasi_id = '" + str(post_data['lokasi_id']) + "' , " \
                    "nama = '" + str(post_data['nama']) + "' " \
                "WHERE user_id = '" + str(user_id[0]) + "'"
        print(sqlLokasiUser)
        cursor = connection.cursor()
        cursor.execute(sqlLokasiUser)
        connection.commit()

        return JsonResponse({"status" : "Sucess"}, status=200)

    def create(self, request):
        post_data = request.data
        print(post_data)
        user = {
            "username": post_data['username'],
            "password": post_data['password'],

        }

        userSerializer = LoginSerializer(data=user)
        if userSerializer.is_valid(self) :
            created = userSerializer.save()
            lokasi_user = {
                "nama": post_data['nama'],
                "lokasi": post_data['lokasi'],
                "user": created.id,
            }
            lokasiUserSerializer = LokasiUserSerializer(data=lokasi_user)
            if lokasiUserSerializer.is_valid(self):
                lokasiUserSerializer.save()


        return Response("Sucess")




# class ReplayTrackViewSet(viewsets.ViewSet):
#     queryset = Sessions.objects.raw("select id, extract(epoch from (end_time::timestamp - start_time::timestamp)) as durasi " \
#           " from sessions " \
#           "WHERE end_time IS NOT null")
#     serializers = SessionsSerializer
#     def list(self, request):
#         '''Get data session yang sudah selesai'''
#         sql = "select id, to_char (start_time::timestamp, 'YYYY-MM-DD HH24:MI:SS') start_time, " \
#               " to_char (end_time::timestamp, 'YYYY-MM-DD HH24:MI:SS') end_time, " \
#               "extract(epoch from (end_time::timestamp - start_time::timestamp)) as durasi " \
#               " from sessions " \
#               "WHERE end_time IS NOT null"
#         query = Sessions.objects.raw(sql)
#         track = []
#         for data in query:
#             '''Buat panjang durasi dibagi dengan UPDATE_RATE. Buat list sesuai dengan panjang_replay'''
#             panjang_replay = data.durasi / UPDATE_RATE
#             track_list = [i for i in range(int(panjang_replay))]
#             track_list = dict.fromkeys(track_list, "")
#             result={
#                     'session_id'        : data.id,
#                     'update_rate'       : UPDATE_RATE,
#                     'start_time'        : str(data.start_time),
#                     'end_time'          : str(data.end_time),
#                     'durasi_session'    : data.durasi,
#                     'track_play'        : track_list
#             }
#             start_time = (datetime.strptime(str(data.start_time), '%Y-%m-%d %H:%M:%S'))
#             end_time = (datetime.strptime(str(data.end_time), '%Y-%m-%d %H:%M:%S'))
#             '''Looping sebanyak panjang replay'''
#
#             for t in range(len(track_list)+1):
#                 '''Buat start_time dan end_time untuk setiap segmen replay.
#                     Segmen durasi adalah satuan  replay track,
#                     contoh 2020-01-10 14:45:31 sampai dengan 2020-01-10 14:45:41
#                     disebut sebagai 1 segmen durasi'''
#                 track_data = []
#                 # print(t)
#                 # print(str(start_time) + " sampai dengan " + str(end_time))
#                 if t == 0:
#                     tmp_time = (datetime.strptime(str(data.start_time), '%Y-%m-%d %H:%M:%S'))
#                     tmp_time += dt.timedelta(seconds=UPDATE_RATE)
#                     end_time = tmp_time
#                 else:
#                     start_time += dt.timedelta(seconds=UPDATE_RATE)
#                     end_time += dt.timedelta(seconds=UPDATE_RATE)
#                 '''Jalankan query untuk setiap tabel per setiap segmen durasi'''
#                 query_tf = "SELECT s.id, tf.* " \
#                                "FROM tactical_figures tf " \
#                                 "JOIN sessions s on tf.session_id = s.id " \
#                                "JOIN(" \
#                                "     SELECT object_id,max(last_update_time) last_update_time " \
#                                "     FROM tactical_figures " \
#                                "     WHERE session_id = " + str(data.id) + " AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
#                                 "     GROUP BY object_id) mx " \
#                                 "ON tf.object_id=mx.object_id and tf.last_update_time=mx.last_update_time " \
#                                 "WHERE tf.session_id = '"+str(data.id)+"' AND tf.last_update_time > '"+str(start_time)+"' AND tf.last_update_time < '"+str(end_time)+"' " \
#                                 "ORDER BY tf.object_id"
#                 for tf in TacticalFigures.objects.raw(query_tf):
#                     tf_status = 'F'+str(tf.object_id)+'R' if tf.is_visible == 'REMOVE' else 'F'+str(tf.object_id)
#                     track_data.append(tf_status)
#
#                 query_rp = "SELECT s.id, rrp.* " \
#                            "FROM replay_reference_point rrp " \
#                            "JOIN sessions s on s.id = rrp.session_id " \
#                            "JOIN (" \
#                            "    SELECT object_id,max(last_update_time) last_update_time " \
#                            "    FROM replay_reference_point " \
#                            "    WHERE session_id = " + str(data.id) + " AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
#                            "    GROUP BY object_id" \
#                            ") mx ON rrp.object_id=mx.object_id and rrp.last_update_time=mx.last_update_time" \
#                            " WHERE rrp.session_id = '"+str(data.id)+"' AND rrp.last_update_time > '"+str(start_time)+"' AND rrp.last_update_time < '"+str(end_time)+"' " \
#                            "ORDER BY rrp.object_id"
#                 for rp in ReplayReferencePoint.objects.raw(query_rp):
#                     rp_status = 'P' + str(rp.object_id)+'R' if rp.visibility_type == 'REMOVE' else 'P'+str(rp.object_id)
#                     track_data.append(rp_status)
#
#                 query_aa = "SELECT aa.session_id as id, aa.* " \
#                             " FROM area_alerts aa " \
#                             " JOIN (" \
#                             "    SELECT object_id,max(last_update_time) last_update_time " \
#                             "    FROM area_alerts " \
#                             "    WHERE session_id = '" + str(data.id) + "' AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
#                             "    GROUP BY object_id " \
#                             ") mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time " \
#                             " WHERE aa.session_id = '" + str(data.id) + "' " \
#                              " AND aa.last_update_time > '"+str(start_time)+"' AND aa.last_update_time < '"+str(end_time)+"' " \
#                              " ORDER BY aa.object_id"
#                 # query_aa = "SELECT aa.session_id as id, aa.*  FROM area_alerts aa  JOIN (    SELECT object_id,max(last_update_time) last_update_time     FROM area_alerts     WHERE session_id = '1' AND last_update_time > '2020-01-10 14:14:31' AND last_update_time < '2020-01-10 14:14:41'     GROUP BY object_id ) mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time  WHERE aa.session_id = '1'  AND aa.last_update_time > '2020-01-10 14:14:31' AND aa.last_update_time < '2020-01-10 14:14:41'  ORDER BY aa.object_id"
#                 print(len(ReplayReferencePoint.objects.raw(query_aa)))
#                 for a in AreaAlerts.objects.raw(query_aa):
#                     aa_status = 'AA' + str(a.object_id)+'R' if a.is_visible == 'REMOVE' else 'AA'+str(a.object_id)
#                     track_data.append(aa_status)
#
#                 result['track_play'][t] = track_data
#
#
#             track.append(result)
#         return Response(track, status=status.HTTP_201_CREATED)
#
# class ReplaySystemTrackProcessingViewSet(viewsets.ModelViewSet):
#     # queryset = ReplaySystemTrackProcessing.objects.all()
#     # serializer_class = ReplaySystemTrackProcessingSerializer
#     queryset = ReplaySystemTrackProcessing.objects.raw(
#         'SELECT session_id as id, * FROM replay_system_track_general')
#     serializer_class = ReplaySystemTrackProcessingSerializer
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_system_track_general'
#         if 'rstp' in cache:
#             # get results from cache
#             products = cache.get('rstp')
#             return Response(products, status=status.HTTP_201_CREATED)
#         else:
#             serialized = []
#             for p in ReplaySystemTrackProcessing.objects.raw(query):
#                 data = {'session_id': p.id, 'nama': p.system_track_number}
#                 serialized.append(data)
#             # store data in cache
#             cache.set('rstp', serialized, timeout=CACHE_TTL)
#             return Response(serialized, status=status.HTTP_201_CREATED)
#
# class TacticalFigureListViewSet(viewsets.ModelViewSet):
#     queryset = TacticalFigureList.objects.all().order_by('-object_id')
#     serializer_class = TacticalFigureListSerializer
#     def list(self, request, *args, **kwargs):
#         results = []
#         if 'tactical_figure_list' in cache:
#             temp            = cache.get('tactical_figure_list')
#             if cache.get('tfl_status') == 'UPDATE':
#                 latest_updates  = TacticalFigureList.objects.order_by('-last_update_time').distinct('object_id')
#                 if temp['last_update_time'] != latest_updates['last_update_time']:
#                     print('send with websocket')
#             results = temp
#         else:
#             tactical_figure_list = self.queryset
#             results = [tfl.to_json() for tfl in tactical_figure_list]
#             cache.set('tactical_figure_list', results, timeout=CACHE_TTL)
#             TFL_STATUS = 'CREATE' if 'tfl_status' not in cache else 'UPDATE'
#             cache.set('tfl_status', TFL_STATUS)
#         return Response(results, status=status.HTTP_200_OK)
#
#
# class GetRealtimeTrackViewSet(viewsets.ViewSet):
#     # queryset = ReplaySystemTrackProcessing.objects.all()
#     # serializer_class = ReplaySystemTrackProcessingSerializer
#     # channel_layer = channels.layers.get_channel_layer()
#     # # Send message to WebSocket
#     # async_to_sync(channel_layer.send)(text_data=json.dumps(
#     #     {"message": "dunia"}
#     # ))
#
#     # channel_layer = get_channel_layer()
#     # loop = asyncio.get_event_loop()
#     #
#     # coroutine = async_to_sync(channel_layer.group_send)(
#     #     'chat_queen',
#     #     {
#     #         'message': 'send_message',
#     #
#     #     }
#     # )
#     # loop.run_until_complete(coroutine)
#     query = "SELECT st.* " \
#             "FROM replay_system_track_general st " \
#             "JOIN sessions s ON st.session_id=s.id JOIN (" \
#             "   SELECT session_id,system_track_number,max(created_time) created_time " \
#             "   FROM replay_system_track_general GROUP BY session_id,system_track_number" \
#             ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
#             "WHERE s.end_time is NULL and st.own_unit_indicator='FALSE' " \
#             "ORDER BY st.system_track_number"
#     queryset            = ReplaySystemTrackGeneral.objects.raw(query)
#     serializer_class    = ReplaySystemTrackProcessingSerializer
#     ar_mandatory_table  = ['replay_system_track_general',
#                            'replay_system_track_kinetic',
#                           'replay_system_track_processing',
#                           'replay_track_general_setting']
#     ar_mandatory_table_8 = ['replay_system_track_general',
#                             'replay_system_track_kinetic',
#                             'replay_system_track_processing',
#                             'replay_system_track_identification',
#                             'replay_system_track_link',
#                             'replay_system_track_mission',
#                             'replay_track_general_setting',
#                             'replay_ais_data']
#     ar_dis_track_number_mandatory_table = [[], [], [], []]
#     ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
#     last_system_track_number_kirim_datetime = ['0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
#                                                '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
#                                                '0000-00-00 00:00:00', '0000-00-00 00:00:00']
#
#     # def create(self, request, *args, **kwargs):
#     #     query = "INSERT INTO replay_system_track_processing(session_id, system_track_number, track_fusion_status, track_join_status, daughter_tracks, track_phase_type, track_suspect_level, created_time) " \
#     #             " VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
#     #     if 'rstp' not in cache:
#     #         products = cache.get('rstp')
#
#
#
#
#     def list(self, request):
#         channel_layer = channels.layers.get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'chat_queen',
#             {
#                 'type': 'chat_message',
#                 'message': 'Ini dari viewset'
#             },
#         )
#         query           = self.query
#         mandatory_table = self.ar_mandatory_table
#
#
#
#         for table in range(len(mandatory_table)):
#             results = []
#             if table not in cache:
#                 cache.set(table, 'kosongan', timeout=CACHE_TTL)
#                 exist = 0
#
#             if ('replay_system_track_general' in cache and
#                     'replay_system_track_kinetic' in cache and
#                     'replay_system_track_processing' in cache and
#                     'replay_track_general_setting' in cache):
#                 results = cache.get(table)
#                 exist = 1
#                 # return Response(results, status=status.HTTP_201_CREATED)
#
#
#
#             if (table == 'replay_system_track_general'):
#                 query = "SELECT s.id as id, st.* " \
#                         "FROM " + self.ar_mandatory_table[table] + " st " \
#                         "JOIN sessions s ON st.session_id=s.id JOIN (" \
#                         "   SELECT session_id,system_track_number,max(created_time) created_time " \
#                         "   FROM replay_system_track_general " \
#                         "   GROUP BY session_id,system_track_number" \
#                         ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
#                         "WHERE s.end_time is NULL and st.own_unit_indicator='FALSE' " \
#                         "ORDER BY st.system_track_number"
#             else:
#                 query = "SELECT s.id as id, st.* " \
#                         "FROM " + self.ar_mandatory_table[table] + " st " \
#                         "JOIN sessions s ON st.session_id=s.id JOIN (" \
#                         "   SELECT session_id,system_track_number,max(created_time) created_time " \
#                         "   FROM replay_system_track_general " \
#                         "   GROUP BY session_id,system_track_number" \
#                         ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
#                         "WHERE s.end_time is NULL " \
#                         "ORDER BY st.system_track_number"
#             # print(query)
#
#             hasil = ReplaySystemTrackGeneral.objects.raw(query)
#             session_id = 0
#             system_track_number = 0
#             # print(self.ar_mandatory_table[table])
#             for p in hasil:
#                 # print(p[0])
#                 self.ar_dis_track_number_mandatory_table[table].append(p.system_track_number)
#                 session_id          = p.id
#                 system_track_number = p.system_track_number
#
#                 # data = {'session_id': p.id, 'nama': p.system_track_number}
#
#                 # serialized.append(data)
#             # cek_data_lengkap = len(set(self.ar_dis_track_number_mandatory_table_pjg))
#             exist = 1
#             if table not in cache:
#                 cache.set(table, 'kosongan', timeout=CACHE_TTL)
#                 # exist=0
#
#             # if ('replay_system_track_general' in cache and
#             #         'replay_system_track_kinetic' in cache and
#             #         'replay_system_track_processing' in cache and
#             #         'replay_track_general_setting' in cache):
#             #     exist=1
#             if (exist == 1):
#                 ar_temp = list(self.ar_dis_track_number_mandatory_table[0])
#                 ar_temp.sort(reverse=True)
#                 # array yang pertama adalah id terakhir
#                 columns = (
#                     'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name',
#                     'iu_indicator',
#                     'airborne_indicator')
#
#                 for ix in range(len(self.ar_mandatory_table_8)):
#                     q = "SELECT s.id, max(r.created_time) created_time FROM " + self.ar_mandatory_table_8[ix];
#                     q = q + " r JOIN sessions s ON s.id = r.session_id WHERE r.session_id = " + str(session_id) + \
#                         " AND system_track_number = " + str(
#                         system_track_number) + "GROUP BY created_time, s.id";
#
#                     created_time = ''
#                     for row in ReplaySystemTrackProcessing.objects.raw(q):
#                         created_time = str(row.created_time)
#                     # dapatkan created time yang terakhir per 8 tabel tersebut
#                     q = "SELECT max(created_time) created_time FROM " + self.ar_mandatory_table_8[ix];
#                     q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(
#                         system_track_number);
#                     if (created_time > str(self.last_system_track_number_kirim_datetime[ix])):
#                         # kirimkan data dengan created time terbaru
#                         # dan simpan ke last_system_track_number_kirim
#                         self.last_system_track_number_kirim_datetime[ix] = created_time
#                     print(session_id)
#                     if (self.ar_mandatory_table_8[ix] == 'replay_system_track_general'):
#                         q = "SELECT s.id, source FROM replay_system_track_general r " \
#                             " JOIN sessions s on r.session_id=s.id " \
#                             "WHERE r.session_id = " + str(
#                                     session_id) + " AND r.system_track_number = " + str(system_track_number);
#                         if self.last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
#                             q = q + " AND r.created_time = null"
#                         else:
#                             q = q + " AND r.created_time = '" + self.last_system_track_number_kirim_datetime[
#                                 ix] + "'"
#
#                         for data_source in ReplaySystemTrackGeneral.objects.raw(q):
#                             if data_source.source == 'AIS_TYPE':
#                                 query = "SELECT s.id, r.system_track_number,r.created_time,identity,environment,source,track_name,iu_indicator" \
#                                         "FROM ";
#                                 query = query + self.ar_mandatory_table_8[
#                                     ix] + " r join sessions s on s.id = r.session_id " \
#                                           "LEFT OUTER JOIN replay_ais_data b on r.system_track_number = b.system_track_number " \
#                                           "WHERE r.session_id = " + str(
#                                     session_id) + " AND r.system_track_number = " + str(system_track_number)
#                                 if self.last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
#                                     query = query + " AND r.created_time = null"
#                                 else:
#                                     query = query + " AND r.created_time = '" + self.last_system_track_number_kirim_datetime[
#                                         ix] + "'"
#                                 print(query)
#                             else:
#                                 query = "SELECT s.id, system_track_number,created_time,identity,environment,source,track_name,iu_indicator  FROM ";
#                                 query = query + self.ar_mandatory_table_8[ix] + " r join sessions s on s.id = r.session_id WHERE session_id = " + str(
#                                     session_id) + " AND system_track_number = " + str(system_track_number);
#                                 if self.last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
#                                     query = query + " AND created_time = null"
#                                 else:
#                                     query = query + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'"
#
#                             for row in Sessions.objects.raw(query):
#                                 data = []
#                                 data.append(row.system_track_number)
#                                 data.append(row.created_time)
#                                 data.append(row.identity)
#                                 data.append(row.environment)
#                                 data.append(row.source)
#                                 data.append(row.track_name)
#                                 data.append(row.iu_indicator)
#
#                                     # print(row)
#                             results.append(dict(zip(columns, data)))
#                         # hasil = json.dumps(results, indent=2, default=str)
#                         # return Response(results, status=status.HTTP_201_CREATED)
#
#                     if (self.ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
#                         q = "SELECT a.session_id as id, latitude,longitude,speed_over_ground,course_over_ground, " \
#                             "b.name as ship_name, b.type_of_ship_or_cargo as type_of_ship, c.source  FROM ";
#                         q = q + self.ar_mandatory_table_8[ix] + " a LEFT OUTER JOIN replay_ais_data b ON a.system_track_number = b.system_track_number " \
#                                                                 "LEFT OUTER JOIN replay_system_track_general c on a.system_track_number = c.system_track_number " \
#                                                                 " WHERE a.session_id = " + str(
#                             session_id) + " AND a.system_track_number = " + str(system_track_number);
#                         q = q + " AND a.created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";
#
#                         for row in ReplaySystemTrackKinetic.objects.raw(q):
#                             results[len(results) - 1]['latitude']           = row.latitude
#                             results[len(results) - 1]['longitude']          = row.longitude
#                             results[len(results) - 1]['speed_over_ground']  = row.speed_over_ground
#                             results[len(results) - 1]['course_over_ground'] = row.course_over_ground
#                             results[len(results) - 1]['ship_name']          = row.ship_name
#                             results[len(results) - 1]['type_of_ship']       = row.type_of_ship
#                             results[len(results) - 1]['source']       = row.source
#
#                         # hasil = json.dumps(results, indent=2, default=str)
#                         return Response(results, status=status.HTTP_201_CREATED)
#
#                     if (self.ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
#                         q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
#                         q = q + self.ar_mandatory_table_8[ix] + " LEFT OUTER JOIN replay_system_track_general ON WHERE session_id = " + str(
#                             session_id) + " AND system_track_number = " + str(system_track_number);
#                         q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";
#                         print(q)
#
#                         for row in ReplaySystemTrackProcessing.objects.raw(q):
#                             results[len(results) - 1]['track_join_status'] = row.rack_join_status
#                             results[len(results) - 1]['track_fusion_status'] = row.track_fusion_status
#                             results[len(results) - 1]['track_phase'] = row.track_phase
#
#                         # hasil = json.dumps(results, indent=2, default=str)
#                         # return Response(results, status=status.HTTP_201_CREATED)
#
#                     if (self.ar_mandatory_table_8[ix] == 'replay_ais_data'):
#                         icek_ais = 0
#                         if (self.last_system_track_number_kirim_datetime[ix] != 'None'):
#                             q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
#                             q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                                 session_id) + " AND system_track_number = " + str(system_track_number);
#                             q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";
#
#
#                             for row in ReplayAisData.objects.raw(q):
#                                 results[len(results) - 1]['type_of_ship_or_cargo'] = row.type_of_ship_or_cargo
#                                 results[len(results) - 1]['ship_name'] = row.ship_name
#                                 icek_ais = 1
#
#                         else:
#                             q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
#                             q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                                 session_id) + " AND system_track_number = " + str(system_track_number);
#                             q = q + " ORDER BY created_time DESC ) aa LIMIT 1";
#
#
#                             for row in Sessions.objects.raw(q):
#                                 results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
#                                 results[len(results) - 1]['ship_name'] = row[1]
#                                 icek_ais = 1
#
#                         if (icek_ais == 0):
#                             results[len(results) - 1]['type_of_ship_or_cargo'] = '-'
#                             results[len(results) - 1]['ship_name'] = '-'
#                         print(q)
#                         # hasil = json.dumps(results, indent=2, default=str)
#                         # return Response(results, status=status.HTTP_201_CREATED)
#
#                     if (self.ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
#                         q = "SELECT track_visibility FROM ";
#                         q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                             session_id) + " AND system_track_number = " + str(system_track_number);
#                         q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";
#
#                         for row in ReplayTrackGeneralSetting.objects.raw(q):
#                             results[len(results) - 1]['track_visibility'] = row[0]
#             # store data in cache
#
#             # cache.set('rstp', serialized, timeout=CACHE_TTL)
#         # return Response(serialized, status=status.HTTP_201_CREATED)
#         print(results)
#         return Response(results, status=status.HTTP_200_OK)
#         # if 'rstp' in cache and 'rstk' in cache and 'rstg' in cache and 'rtgs' in cache:
#         #     # get results from cache
#         #     products = cache.get('rstp')
#         #     return Response(products, status=status.HTTP_201_CREATED)
#         # else:
#
#
#
#
#
# class ReplaySystemTrackKineticViewSet(viewsets.ViewSet):
#     # queryset = ReplaySystemTrackKinetic.objects.all()
#     # serializer_class = ReplaySystemTrackKineticSerializer
#     queryset = ReplaySystemTrackKinetic.objects.raw(
#          'SELECT session_id as id, * FROM replay_system_track_kinetic')
#     serializer_class = ReplaySystemTrackKineticSerializer
#
#     def list(self, request):
#         if 'rstk' in cache:
#             # get results from cache
#             products = cache.get('rstk')
#             return Response(products, status=status.HTTP_201_CREATED)
#
#         else:
#             products = ReplaySystemTrackKinetic.objects.raw(
#                         'SELECT session_id as id, * FROM replay_system_track_kinetic')
#             serialized = []
#             for p in products:
#                 data = {'session_id': p.id, 'nama': p.track_name}
#                 serialized.append(data)
#             # return Response(serialized)
#             # results = [product.to_json() for product in products]
#             # store data in cache
#             cache.set('rstk', serialized, timeout=CACHE_TTL)
#             return Response(serialized, status=status.HTTP_201_CREATED)
#         # query = 'SELECT session_id as id, * FROM replay_system_track_kinetic'
#
#
# class ReferencePointsViewSet(viewsets.ModelViewSet):
#     # queryset = ReferencePoints.objects.all()
#
#     serializer_class = ReferencePointsSerializer
#     model = ReferencePoints
#
#     def list(self, request, *args, **kwargs):
#         # serialized      = serializer(queryset, many=True)
#         # print(serialized.data[2].get('name'))
#         query = 'SELECT session_id as id, * FROM reference_point'
#         serialized = []
#         for p in ReplayAisData.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.name}
#             serialized.append(data)
#         return Response(serialized)
#
# class ReplayAisDataViewSet(viewsets.ModelViewSet):
#     # queryset = ReplayAisData.objects.all()
#     # queryset = ReplayAisData.objects.filter('imo_number')
#     model               = ReplayAisData
#     serializer_class    = ReplayAisDataSerializer
#     queryset            = ReplayAisData.objects.raw('SELECT session_id as id, * FROM replay_ais_data')
#
#
#     def list(self, request, *args, **kwargs):
#         # serialized      = serializer(queryset, many=True)
#         # print(serialized.data[2].get('name'))
#         query = 'SELECT session_id as id, * FROM replay_ais_data'
#         serialized = []
#         for p in ReplayAisData.objects.raw(query):
#             data = {'session_id': p.id, 'nama' : p.name}
#             serialized.append(data)
#         return Response(serialized)
#         # return ReplayAisData.object.raw("SELECT * FROM replay_ais_data")
#
# class ReplayReferencePointViewSet(viewsets.ModelViewSet):
#     # queryset = ReplayReferencePoint.objects.all()
#     serializer_class = ReplayReferencePointSerializer
#     model = ReplayReferencePoint
#     queryset = ReplayReferencePoint.objects.raw('SELECT session_id as id, * FROM replay_reference_point')
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_reference_point'
#         serialized = []
#         for p in ReplayReferencePoint.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.name}
#             serialized.append(data)
#         return Response(serialized)
#
# class ReplaySystemTrackGeneralViewSet(viewsets.ModelViewSet):
#     queryset = ReplaySystemTrackGeneral.objects.raw('SELECT session_id as id, track_name FROM replay_system_track_general')
#     serializer_class = ReplaySystemTrackGeneralSerializer
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_system_track_general'
#         serialized = []
#
#         for p in ReplaySystemTrackGeneral.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.track_name}
#             serialized.append(data)
#         # results = [s.to_json for s in serialized]
#         cache.set(serialized, serialized, timeout=CACHE_TTL)
#         return Response(serialized)
#
# class ReplaySystemTrackIdentificationViewSet(viewsets.ModelViewSet):
#     # queryset = ReplaySystemTrackIdentification.objects.all()
#     # serializer_class = ReplaySystemTrackIdentificationSerializer
#     queryset = ReplaySystemTrackIdentification.objects.raw(
#         'SELECT session_id as id, * FROM replay_system_track_identification')
#     serializer_class = ReplaySystemTrackIdentificationSerializer
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_system_track_general'
#         serialized = []
#         for p in ReplaySystemTrackIdentification.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.system_track_number}
#             serialized.append(data)
#         return Response(serialized)
#     # def list(self, request):
#     #     # queryset = ReplaySystemTrackIdentification.objects.raw('SELECT * FROM replay_system_track_identification')
#     #     # serializer = ReplaySystemTrackIdentification(queryset, many=True)
#     #     serializer = ReplaySystemTrackIdentificationSerializer(
#     #         instance=ReplaySystemTrackIdentification.values(), many=True)
#     #     return Response(serializer.data)
#
# class SendData(viewsets.ViewSet):
#     def list(self, request):
#         ar_mandatory_table = ['replay_system_track_general', 'replay_system_track_kinetic',
#                               'replay_system_track_processing',
#                               'replay_track_general_setting']
#         ar_mandatory_table_8 = ['replay_system_track_general', 'replay_system_track_kinetic',
#                                 'replay_system_track_processing',
#                                 'replay_system_track_identification', 'replay_system_track_link',
#                                 'replay_system_track_mission',
#                                 'replay_track_general_setting', 'replay_ais_data']
#         ar_dis_track_number_mandatory_table = [[], [], [], []]
#         ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
#         for ix in range(len(ar_mandatory_table)):
#             print(ix, ar_mandatory_table[ix])
#             if (ar_mandatory_table[ix] == 'replay_system_track_general'):
#                 q = "SELECT st.system_track_number,mx.created_time,st.session_id FROM " + ar_mandatory_table[
#                     ix] + " st JOIN sessions s ON st.session_id=s.id JOIN (SELECT session_id,system_track_number,max(created_time) created_time FROM " + \
#                     ar_mandatory_table[
#                         ix] + " GROUP BY session_id,system_track_number) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id WHERE s.end_time is NULL AND st.own_unit_indicator='FALSE' ORDER BY st.system_track_number;";
#             else:
#                 q = "SELECT st.system_track_number,mx.created_time,st.session_id  FROM " + ar_mandatory_table[
#                     ix] + " st JOIN sessions s ON st.session_id=s.id JOIN (SELECT session_id,system_track_number,max(created_time) created_time FROM " + \
#                     ar_mandatory_table[
#                         ix] + " GROUP BY session_id,system_track_number) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id WHERE s.end_time is NULL ORDER BY st.system_track_number;";
#
#             for p in ReplaySystemTrackKinetic.objects.raw(q):
#                 ar_dis_track_number_mandatory_table[ix].append(p[0])
#                 session_id = p[2]
#                 system_track_number = p[0]
#
#             ar_dis_track_number_mandatory_table_pjg[ix] = len(ar_dis_track_number_mandatory_table[ix])
#             cek_data_lengkap = len(set(ar_dis_track_number_mandatory_table_pjg))
#             if (cek_data_lengkap == 1):
#                 # maka sama artinya data dari 4 tabel mandatory sudah bisa dikirimkan
#                 # untuk mendapatkan nilai terakhir
#                 ar_temp = list(ar_dis_track_number_mandatory_table[0])
#                 ar_temp.sort(reverse=True)
#                 # array yang pertama adalah id terakhir
#                 print('id terakhir = ', ar_temp[0])
#                 # cari created_time untuk id terakhir tersebut
#                 print('session id = ', session_id)
#                 print('system_track_number = ', system_track_number)
#                 # 3. cek apakah sudah dikirimkan dari tabel track general 2 kondisi
#                 # 3. jika system track number > yg ada di memory
#
#                 columns = (
#                     'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name',
#                     'iu_indicator',
#                     'airborne_indicator')
#                 results = []
#                 for ix in range(len(ar_mandatory_table_8)):
#                     # dapatkan created time yang terakhir per 8 tabel tersebut
#                     q = "SELECT max(created_time) created_time FROM " + ar_mandatory_table_8[ix];
#                     q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(
#                         system_track_number);
#                     # cur.execute(q)
#                     # data = cur.fetchall()
#                     # for row in data:
#                     #     created_time = str(row[0])
#
#                     # if (created_time > str(last_system_track_number_kirim_datetime[ix])):
#                     #     # kirimkan data dengan created time terbaru
#                     #     # dan simpan ke last_system_track_number_kirim
#                     #     last_system_track_number_kirim_datetime[ix] = created_time
#                     #
#                     # if (ar_mandatory_table_8[ix] == 'replay_system_track_general'):
#                     #
#                     #     q = "SELECT system_track_number,created_time,identity,environment,source,track_name,iu_indicator,airborne_indicator  FROM ";
#                     #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #         session_id) + " AND system_track_number = " + str(system_track_number);
#                     #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
#                     #     cur.execute(q)
#                     #     for row in cur.fetchall():
#                     #         results.append(dict(zip(columns, row)))
#                     #     hasil = json.dumps(results, indent=2, default=str)
#                     #
#                     # if (ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
#                     #     q = "SELECT latitude,longitude,speed_over_ground,course_over_ground FROM ";
#                     #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #         session_id) + " AND system_track_number = " + str(system_track_number);
#                     #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
#                     #     cur.execute(q)
#                     #     for row in cur.fetchall():
#                     #         results[len(results) - 1]['latitude'] = row[0]
#                     #         results[len(results) - 1]['longitude'] = row[1]
#                     #         results[len(results) - 1]['speed_over_ground'] = row[2]
#                     #         results[len(results) - 1]['course_over_ground'] = row[3]
#                     #
#                     #     hasil = json.dumps(results, indent=2, default=str)
#                     #
#                     # if (ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
#                     #     q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
#                     #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #         session_id) + " AND system_track_number = " + str(system_track_number);
#                     #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
#                     #     cur.execute(q)
#                     #     for row in cur.fetchall():
#                     #         results[len(results) - 1]['track_join_status'] = row[0]
#                     #         results[len(results) - 1]['track_fusion_status'] = row[1]
#                     #         results[len(results) - 1]['track_phase'] = row[2]
#                     #
#                     #     hasil = json.dumps(results, indent=2, default=str)
#                     #
#                     # if (ar_mandatory_table_8[ix] == 'replay_ais_data'):
#                     #     icek_ais = 0
#                     #     if (last_system_track_number_kirim_datetime[ix] != 'None'):
#                     #         q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
#                     #         q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #             session_id) + " AND system_track_number = " + str(system_track_number);
#                     #         q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
#                     #
#                     #         cur.execute(q)
#                     #         for row in cur.fetchall():
#                     #             results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
#                     #             results[len(results) - 1]['ship_name'] = row[1]
#                     #             icek_ais = 1
#                     #
#                     #     else:
#                     #         q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
#                     #         q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #             session_id) + " AND system_track_number = " + str(system_track_number);
#                     #         q = q + " ORDER BY created_time DESC ) aa LIMIT 1";
#                     #
#                     #         cur.execute(q)
#                     #         for row in cur.fetchall():
#                     #             results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
#                     #             results[len(results) - 1]['ship_name'] = row[1]
#                     #             icek_ais = 1
#                     #
#                     #     if (icek_ais == 0):
#                     #         results[len(results) - 1]['type_of_ship_or_cargo'] = '-'
#                     #         results[len(results) - 1]['ship_name'] = '-'
#                     #     print(q)
#                     #     hasil = json.dumps(results, indent=2, default=str)
#                     #
#                     # if (ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
#                     #     q = "SELECT track_visibility FROM ";
#                     #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
#                     #         session_id) + " AND system_track_number = " + str(system_track_number);
#                     #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
#                     #     cur.execute(q)
#                     #     for row in cur.fetchall():
#                     #         results[len(results) - 1]['track_visibility'] = row[0]
#                     #
#                     #     hasil = json.dumps(results, indent=2, default=str)
#             return Response('siap ndan')
#
#
#         return Response({'message' : 'just wait'});
#
#
# class ReplaySystemTrackLinkViewSet(viewsets.ModelViewSet):
#     # queryset = ReplaySystemTrackLink.objects.all()
#     # serializer_class = ReplaySystemTrackLinkSerializer
#     queryset = ReplaySystemTrackLink.objects.raw(
#         'SELECT session_id as id, * FROM replay_system_track_link')
#     serializer_class = ReplaySystemTrackLinkSerializer
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_system_track_link'
#         serialized = []
#         for p in ReplaySystemTrackLink.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.system_track_number}
#             serialized.append(data)
#         return Response(serialized)
#
# class ReplaySystemTrackMissionViewSet(viewsets.ModelViewSet):
#     # queryset = ReplaySystemTrackMission.objects.all()
#     # serializer_class = ReplaySystemTrackMissionSerializer
#     queryset = ReplaySystemTrackMission.objects.raw(
#         'SELECT session_id as id, * FROM replay_system_track_mission')
#     serializer_class = ReplaySystemTrackMissionSerializer
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_system_track_mission'
#         serialized = []
#         for p in ReplaySystemTrackMission.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.system_track_number}
#             serialized.append(data)
#         return Response(serialized)
#
#
#
# class ReplayTrackGeneralSettingViewSet(viewsets.ModelViewSet):
#     # queryset = ReplayTrackGeneralSetting.objects.all()
#     # serializer_class = ReplayTrackGeneralSettingSerializer
#     queryset = ReplayTrackGeneralSetting.objects.raw(
#         'SELECT session_id as id, * FROM replay_track_general_setting')
#     serializer_class = ReplayTrackGeneralSettingSerializer
#
#     def list(self, request):
#         query = 'SELECT session_id as id, * FROM replay_track_general_setting'
#         serialized = []
#         for p in ReplayTrackGeneralSetting.objects.raw(query):
#             data = {'session_id': p.id, 'nama': p.system_track_number}
#             serialized.append(data)
#         return Response(serialized)
#
#
# class SessionsViewSet(viewsets.ModelViewSet):
#     queryset = Sessions.objects.all()
#     serializer_class = SessionsSerializer
#
#
#
# class TacticalFiguresViewSet(viewsets.ModelViewSet):
#     queryset = TacticalFigures.objects.all()
#     serializer_class = TacticalFiguresSerializer
#
# class AreaAlertViewSet(viewsets.ModelViewSet):
#     queryset = AreaAlerts.objects.all()
#     serializer_class = AreaAlertsSerializer
#
