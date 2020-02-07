from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from c2shiptrack.unusedmodels import *
from .serializer import *
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class GetRealtimeTrackViewSet(viewsets.ViewSet):
    # queryset = ReplaySystemTrackProcessing.objects.all()
    # serializer_class = ReplaySystemTrackProcessingSerializer
    query = "SELECT st.* " \
            "FROM replay_system_track_general st " \
            "JOIN sessions s ON st.session_id=s.id JOIN (" \
            "   SELECT session_id,system_track_number,max(created_time) created_time " \
            "   FROM replay_system_track_general GROUP BY session_id,system_track_number" \
            ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
            "WHERE s.end_time is NULL and st.own_unit_indicator='FALSE' " \
            "ORDER BY st.system_track_number"
    queryset            = ReplaySystemTrackGeneral.objects.raw(query)
    serializer_class    = ReplaySystemTrackProcessingSerializer
    ar_mandatory_table  = ['replay_system_track_general', 'replay_system_track_kinetic',
                          'replay_system_track_processing',
                          'replay_track_general_setting']
    ar_mandatory_table_8 = ['replay_system_track_general', 'replay_system_track_kinetic',
                            'replay_system_track_processing',
                            'replay_system_track_identification', 'replay_system_track_link',
                            'replay_system_track_mission',
                            'replay_track_general_setting', 'replay_ais_data']
    ar_dis_track_number_mandatory_table = [[], [], [], []]
    ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
    last_system_track_number_kirim_datetime = ['0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                               '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                               '0000-00-00 00:00:00', '0000-00-00 00:00:00']

    # def create(self, request, *args, **kwargs):
    #     query = "INSERT INTO replay_system_track_processing(session_id, system_track_number, track_fusion_status, track_join_status, daughter_tracks, track_phase_type, track_suspect_level, created_time) " \
    #             " VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    #     if 'rstp' not in cache:
    #         products = cache.get('rstp')




    def list(self, request):

        query           = self.query
        mandatory_table = self.ar_mandatory_table

        results = []
        for table in range(len(mandatory_table)):
            # if table not in cache:
            #     cache.set(table, 'kosongan', timeout=CACHE_TTL)
            #     exist=0
            #
            # if ('replay_system_track_general' in cache and
            #         'replay_system_track_kinetic' in cache and
            #         'replay_system_track_processing' in cache and
            #         'replay_track_general_setting' in cache):
            #     exist=1
            if (table == 'replay_system_track_general'):
                query = "SELECT s.id as id, st.* " \
                        "FROM " + self.ar_mandatory_table[table] + " st " \
                        "JOIN sessions s ON st.session_id=s.id JOIN (" \
                        "   SELECT session_id,system_track_number,max(created_time) created_time " \
                        "   FROM replay_system_track_general " \
                        "   GROUP BY session_id,system_track_number" \
                        ") mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id " \
                        "WHERE s.end_time is NULL and st.own_unit_indicator='FALSE' " \
                        "ORDER BY st.system_track_number"
            else:
                query = "SELECT s.id as id, st.* " \
                        "FROM " + self.ar_mandatory_table[table] + " st " \
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
            # print(self.ar_mandatory_table[table])
            for p in hasil:
                # print(p[0])
                self.ar_dis_track_number_mandatory_table[table].append(p.system_track_number)
                session_id          = p.id
                system_track_number = p.system_track_number

                # data = {'session_id': p.id, 'nama': p.system_track_number}

                # serialized.append(data)
            # cek_data_lengkap = len(set(self.ar_dis_track_number_mandatory_table_pjg))
            exist = 1
            if table not in cache:
                cache.set(table, 'kosongan', timeout=CACHE_TTL)
                # exist=0

            # if ('replay_system_track_general' in cache and
            #         'replay_system_track_kinetic' in cache and
            #         'replay_system_track_processing' in cache and
            #         'replay_track_general_setting' in cache):
            #     exist=1
            if (exist == 1):
                ar_temp = list(self.ar_dis_track_number_mandatory_table[0])
                ar_temp.sort(reverse=True)
                # array yang pertama adalah id terakhir
                columns = (
                    'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name',
                    'iu_indicator',
                    'airborne_indicator')

                for ix in range(len(self.ar_mandatory_table_8)):
                    q = "SELECT s.id, max(r.created_time) created_time FROM " + self.ar_mandatory_table_8[ix];
                    q = q + " r JOIN sessions s ON s.id = r.session_id WHERE r.session_id = " + str(session_id) + \
                        " AND system_track_number = " + str(
                        system_track_number) + "GROUP BY created_time, s.id";

                    created_time = ''
                    for row in ReplaySystemTrackProcessing.objects.raw(q):
                        created_time = str(row.created_time)
                    # dapatkan created time yang terakhir per 8 tabel tersebut
                    q = "SELECT max(created_time) created_time FROM " + self.ar_mandatory_table_8[ix];
                    q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(
                        system_track_number);
                    if (created_time > str(self.last_system_track_number_kirim_datetime[ix])):
                        # kirimkan data dengan created time terbaru
                        # dan simpan ke last_system_track_number_kirim
                        self.last_system_track_number_kirim_datetime[ix] = created_time

                    if (self.ar_mandatory_table_8[ix] == 'replay_system_track_general'):

                        q = "SELECT s.id, system_track_number,created_time,identity,environment,source,track_name,iu_indicator  FROM ";
                        q = q + self.ar_mandatory_table_8[ix] + " r join sessions s on s.id = r.session_id WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        if self.last_system_track_number_kirim_datetime[ix] == '0000-00-00 00:00:00':
                            q = q + " AND created_time = null";
                        else:
                            q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";

                        for row in Sessions.objects.raw(q):
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

                    if (self.ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
                        q = "SELECT session_id as id, latitude,longitude,speed_over_ground,course_over_ground FROM ";
                        q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";

                        for row in ReplaySystemTrackKinetic.objects.raw(q):
                            results[len(results) - 1]['latitude']           = row.latitude
                            results[len(results) - 1]['longitude']          = row.longitude
                            results[len(results) - 1]['speed_over_ground']  = row.speed_over_ground
                            results[len(results) - 1]['course_over_ground'] = row.course_over_ground

                        # hasil = json.dumps(results, indent=2, default=str)
                        return Response(results, status=status.HTTP_201_CREATED)

                    if (self.ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
                        q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
                        q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";

                        for row in ReplaySystemTrackProcessing.objects.raw(q):
                            results[len(results) - 1]['track_join_status'] = row.rack_join_status
                            results[len(results) - 1]['track_fusion_status'] = row.track_fusion_status
                            results[len(results) - 1]['track_phase'] = row.track_phase

                        # hasil = json.dumps(results, indent=2, default=str)
                        return Response(results, status=status.HTTP_201_CREATED)

                    if (self.ar_mandatory_table_8[ix] == 'replay_ais_data'):
                        icek_ais = 0
                        if (self.last_system_track_number_kirim_datetime[ix] != 'None'):
                            q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                            q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                                session_id) + " AND system_track_number = " + str(system_track_number);
                            q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";


                            for row in ReplayAisData.objects.raw(q):
                                results[len(results) - 1]['type_of_ship_or_cargo'] = row.type_of_ship_or_cargo
                                results[len(results) - 1]['ship_name'] = row.ship_name
                                icek_ais = 1

                        else:
                            q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                            q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
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
                        return Response(results, status=status.HTTP_201_CREATED)

                    if (self.ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
                        q = "SELECT track_visibility FROM ";
                        q = q + self.ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                            session_id) + " AND system_track_number = " + str(system_track_number);
                        q = q + " AND created_time = '" + self.last_system_track_number_kirim_datetime[ix] + "'";

                        for row in ReplayTrackGeneralSetting.objects.raw(q):
                            results[len(results) - 1]['track_visibility'] = row[0]
            # store data in cache

            # cache.set('rstp', serialized, timeout=CACHE_TTL)
        # return Response(serialized, status=status.HTTP_201_CREATED)
        print(results)
        return Response(results, status=status.HTTP_200_OK)
        # if 'rstp' in cache and 'rstk' in cache and 'rstg' in cache and 'rtgs' in cache:
        #     # get results from cache
        #     products = cache.get('rstp')
        #     return Response(products, status=status.HTTP_201_CREATED)
        # else:



class ReplaySystemTrackProcessingViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackProcessing.objects.all()
    # serializer_class = ReplaySystemTrackProcessingSerializer
    queryset = ReplaySystemTrackProcessing.objects.raw(
        'SELECT session_id as id, * FROM replay_system_track_general')
    serializer_class = ReplaySystemTrackProcessingSerializer

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_system_track_general'
        if 'rstp' in cache:
            # get results from cache
            products = cache.get('rstp')
            return Response(products, status=status.HTTP_201_CREATED)
        else:
            serialized = []
            for p in ReplaySystemTrackProcessing.objects.raw(query):
                data = {'session_id': p.id, 'nama': p.system_track_number}
                serialized.append(data)
            # store data in cache
            cache.set('rstp', serialized, timeout=CACHE_TTL)
            return Response(serialized, status=status.HTTP_201_CREATED)

class ReplaySystemTrackKineticViewSet(viewsets.ViewSet):
    # queryset = ReplaySystemTrackKinetic.objects.all()
    # serializer_class = ReplaySystemTrackKineticSerializer
    queryset = ReplaySystemTrackKinetic.objects.raw(
         'SELECT session_id as id, * FROM replay_system_track_kinetic')
    serializer_class = ReplaySystemTrackKineticSerializer

    def list(self, request):
        if 'rstk' in cache:
            # get results from cache
            products = cache.get('rstk')
            return Response(products, status=status.HTTP_201_CREATED)

        else:
            products = ReplaySystemTrackKinetic.objects.raw(
                        'SELECT session_id as id, * FROM replay_system_track_kinetic')
            serialized = []
            for p in products:
                data = {'session_id': p.id, 'nama': p.track_name}
                serialized.append(data)
            # return Response(serialized)
            # results = [product.to_json() for product in products]
            # store data in cache
            cache.set('rstk', serialized, timeout=CACHE_TTL)
            return Response(serialized, status=status.HTTP_201_CREATED)
        # query = 'SELECT session_id as id, * FROM replay_system_track_kinetic'


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
        # results = [s.to_json for s in serialized]
        cache.set(serialized, serialized, timeout=CACHE_TTL)
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

class SendData(viewsets.ViewSet):
    def list(self, request):
        ar_mandatory_table = ['replay_system_track_general', 'replay_system_track_kinetic',
                              'replay_system_track_processing',
                              'replay_track_general_setting']
        ar_mandatory_table_8 = ['replay_system_track_general', 'replay_system_track_kinetic',
                                'replay_system_track_processing',
                                'replay_system_track_identification', 'replay_system_track_link',
                                'replay_system_track_mission',
                                'replay_track_general_setting', 'replay_ais_data']
        ar_dis_track_number_mandatory_table = [[], [], [], []]
        ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
        for ix in range(len(ar_mandatory_table)):
            print(ix, ar_mandatory_table[ix])
            if (ar_mandatory_table[ix] == 'replay_system_track_general'):
                q = "SELECT st.system_track_number,mx.created_time,st.session_id FROM " + ar_mandatory_table[
                    ix] + " st JOIN sessions s ON st.session_id=s.id JOIN (SELECT session_id,system_track_number,max(created_time) created_time FROM " + \
                    ar_mandatory_table[
                        ix] + " GROUP BY session_id,system_track_number) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id WHERE s.end_time is NULL AND st.own_unit_indicator='FALSE' ORDER BY st.system_track_number;";
            else:
                q = "SELECT st.system_track_number,mx.created_time,st.session_id  FROM " + ar_mandatory_table[
                    ix] + " st JOIN sessions s ON st.session_id=s.id JOIN (SELECT session_id,system_track_number,max(created_time) created_time FROM " + \
                    ar_mandatory_table[
                        ix] + " GROUP BY session_id,system_track_number) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time and st.session_id=mx.session_id WHERE s.end_time is NULL ORDER BY st.system_track_number;";

            for p in ReplaySystemTrackKinetic.objects.raw(q):
                ar_dis_track_number_mandatory_table[ix].append(p[0])
                session_id = p[2]
                system_track_number = p[0]

            ar_dis_track_number_mandatory_table_pjg[ix] = len(ar_dis_track_number_mandatory_table[ix])
            cek_data_lengkap = len(set(ar_dis_track_number_mandatory_table_pjg))
            if (cek_data_lengkap == 1):
                # maka sama artinya data dari 4 tabel mandatory sudah bisa dikirimkan
                # untuk mendapatkan nilai terakhir
                ar_temp = list(ar_dis_track_number_mandatory_table[0])
                ar_temp.sort(reverse=True)
                # array yang pertama adalah id terakhir
                print('id terakhir = ', ar_temp[0])
                # cari created_time untuk id terakhir tersebut
                print('session id = ', session_id)
                print('system_track_number = ', system_track_number)
                # 3. cek apakah sudah dikirimkan dari tabel track general 2 kondisi
                # 3. jika system track number > yg ada di memory

                columns = (
                    'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name',
                    'iu_indicator',
                    'airborne_indicator')
                results = []
                for ix in range(len(ar_mandatory_table_8)):
                    # dapatkan created time yang terakhir per 8 tabel tersebut
                    q = "SELECT max(created_time) created_time FROM " + ar_mandatory_table_8[ix];
                    q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(
                        system_track_number);
                    # cur.execute(q)
                    # data = cur.fetchall()
                    # for row in data:
                    #     created_time = str(row[0])

                    # if (created_time > str(last_system_track_number_kirim_datetime[ix])):
                    #     # kirimkan data dengan created time terbaru
                    #     # dan simpan ke last_system_track_number_kirim
                    #     last_system_track_number_kirim_datetime[ix] = created_time
                    #
                    # if (ar_mandatory_table_8[ix] == 'replay_system_track_general'):
                    #
                    #     q = "SELECT system_track_number,created_time,identity,environment,source,track_name,iu_indicator,airborne_indicator  FROM ";
                    #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #         session_id) + " AND system_track_number = " + str(system_track_number);
                    #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    #     cur.execute(q)
                    #     for row in cur.fetchall():
                    #         results.append(dict(zip(columns, row)))
                    #     hasil = json.dumps(results, indent=2, default=str)
                    #
                    # if (ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
                    #     q = "SELECT latitude,longitude,speed_over_ground,course_over_ground FROM ";
                    #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #         session_id) + " AND system_track_number = " + str(system_track_number);
                    #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    #     cur.execute(q)
                    #     for row in cur.fetchall():
                    #         results[len(results) - 1]['latitude'] = row[0]
                    #         results[len(results) - 1]['longitude'] = row[1]
                    #         results[len(results) - 1]['speed_over_ground'] = row[2]
                    #         results[len(results) - 1]['course_over_ground'] = row[3]
                    #
                    #     hasil = json.dumps(results, indent=2, default=str)
                    #
                    # if (ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
                    #     q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
                    #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #         session_id) + " AND system_track_number = " + str(system_track_number);
                    #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    #     cur.execute(q)
                    #     for row in cur.fetchall():
                    #         results[len(results) - 1]['track_join_status'] = row[0]
                    #         results[len(results) - 1]['track_fusion_status'] = row[1]
                    #         results[len(results) - 1]['track_phase'] = row[2]
                    #
                    #     hasil = json.dumps(results, indent=2, default=str)
                    #
                    # if (ar_mandatory_table_8[ix] == 'replay_ais_data'):
                    #     icek_ais = 0
                    #     if (last_system_track_number_kirim_datetime[ix] != 'None'):
                    #         q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                    #         q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #             session_id) + " AND system_track_number = " + str(system_track_number);
                    #         q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    #
                    #         cur.execute(q)
                    #         for row in cur.fetchall():
                    #             results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
                    #             results[len(results) - 1]['ship_name'] = row[1]
                    #             icek_ais = 1
                    #
                    #     else:
                    #         q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                    #         q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #             session_id) + " AND system_track_number = " + str(system_track_number);
                    #         q = q + " ORDER BY created_time DESC ) aa LIMIT 1";
                    #
                    #         cur.execute(q)
                    #         for row in cur.fetchall():
                    #             results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
                    #             results[len(results) - 1]['ship_name'] = row[1]
                    #             icek_ais = 1
                    #
                    #     if (icek_ais == 0):
                    #         results[len(results) - 1]['type_of_ship_or_cargo'] = '-'
                    #         results[len(results) - 1]['ship_name'] = '-'
                    #     print(q)
                    #     hasil = json.dumps(results, indent=2, default=str)
                    #
                    # if (ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
                    #     q = "SELECT track_visibility FROM ";
                    #     q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    #         session_id) + " AND system_track_number = " + str(system_track_number);
                    #     q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                    #     cur.execute(q)
                    #     for row in cur.fetchall():
                    #         results[len(results) - 1]['track_visibility'] = row[0]
                    #
                    #     hasil = json.dumps(results, indent=2, default=str)
            return Response('siap ndan')


        return Response({'message' : 'just wait'});


class ReplaySystemTrackLinkViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackLink.objects.all()
    # serializer_class = ReplaySystemTrackLinkSerializer
    queryset = ReplaySystemTrackLink.objects.raw(
        'SELECT session_id as id, * FROM replay_system_track_link')
    serializer_class = ReplaySystemTrackLinkSerializer

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_system_track_link'
        serialized = []
        for p in ReplaySystemTrackLink.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.system_track_number}
            serialized.append(data)
        return Response(serialized)

class ReplaySystemTrackMissionViewSet(viewsets.ModelViewSet):
    # queryset = ReplaySystemTrackMission.objects.all()
    # serializer_class = ReplaySystemTrackMissionSerializer
    queryset = ReplaySystemTrackMission.objects.raw(
        'SELECT session_id as id, * FROM replay_system_track_mission')
    serializer_class = ReplaySystemTrackMissionSerializer

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_system_track_mission'
        serialized = []
        for p in ReplaySystemTrackMission.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.system_track_number}
            serialized.append(data)
        return Response(serialized)



class ReplayTrackGeneralSettingViewSet(viewsets.ModelViewSet):
    # queryset = ReplayTrackGeneralSetting.objects.all()
    # serializer_class = ReplayTrackGeneralSettingSerializer
    queryset = ReplayTrackGeneralSetting.objects.raw(
        'SELECT session_id as id, * FROM replay_track_general_setting')
    serializer_class = ReplayTrackGeneralSettingSerializer

    def list(self, request):
        query = 'SELECT session_id as id, * FROM replay_track_general_setting'
        serialized = []
        for p in ReplayTrackGeneralSetting.objects.raw(query):
            data = {'session_id': p.id, 'nama': p.system_track_number}
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

