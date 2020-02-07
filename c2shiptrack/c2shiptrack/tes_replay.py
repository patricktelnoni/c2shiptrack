import psycopg2
import json

conn = psycopg2.connect("dbname=shiptrack user=postgres host=localhost password=1234")
cur = conn.cursor()
# i = 0;
ar_mandatory_table = ['replay_system_track_general', 'replay_system_track_kinetic', 'replay_system_track_processing',
                      'replay_track_general_setting']

'''
Semua table akan redundant kecuali tactical_figure_list dan refrence_points
data akan dikirim ke client jika date_timenya terbaru.
Jika ada data pada mandatory type hanya 2 tabel yang diisi tidak ada updaet yang dikirim

Skenario untuk redundant table: 
Jika 4 mandatory table tidak terisi, tidak ada update yang dikirim
Jika 4 terisi, kirim update ke client.
Jika setelah 4 mandatory data diisi ada, insert data ke dalam salah satu mandatory table,
maka kirim data ke client, jenisnya update.
Jika ada update remove, berarti create yang pertama, diremove, sehingga harus menunggu
4 mandotary table diisi lagi 

'''
ar_mandatory_table_8 = ['replay_system_track_general', 'replay_system_track_kinetic', 'replay_system_track_processing',
                        'replay_system_track_identification', 'replay_system_track_link', 'replay_system_track_mission',
                        'replay_track_general_setting', 'replay_ais_data']
ar_dis_track_number_mandatory_table = [[], [], [], []]
ar_dis_track_number_mandatory_table_pjg = [0, 0, 0, 0]
ar_dis_track_number_mandatory_table_pjg_cr_time = ['-', '-', '-', '-']
last_system_track_number_kirim_datetime = ['0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                           '0000-00-00 00:00:00', '0000-00-00 00:00:00', '0000-00-00 00:00:00',
                                           '0000-00-00 00:00:00', '0000-00-00 00:00:00']
last_system_track_number_kirim = ['-', '-', '-', '-', '-', '-', '-', '-']
print(ar_mandatory_table)

try:
    # 1. ambil distinct data
    # 1.1. looping per mandatory table
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
        print(q)
        cur.execute(q)
        data = cur.fetchall()

        for row in data:
            ar_dis_track_number_mandatory_table[ix].append(row[0])
            session_id = row[2]
            system_track_number = row[0]
            # if(ar_mandatory_table[ix]=='replay_system_track_general'):

        ar_dis_track_number_mandatory_table_pjg[ix] = len(ar_dis_track_number_mandatory_table[ix])

    cek_data_lengkap = len(set(ar_dis_track_number_mandatory_table_pjg))  # kalau sama harusnya 1 angka saja
    # 2. cek kelengkapan data
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
        'system_track_number', 'created_time', 'identity', 'environment', 'source', 'track_name', 'iu_indicator',
        'airborne_indicator')
        results = []
        for ix in range(len(ar_mandatory_table_8)):
            # dapatkan created time yang terakhir per 8 tabel tersebut
            q = "SELECT max(created_time) created_time FROM " + ar_mandatory_table_8[ix];
            q = q + " WHERE session_id = " + str(session_id) + " AND system_track_number = " + str(system_track_number);
            cur.execute(q)
            data = cur.fetchall()
            for row in data:
                created_time = str(row[0])

            if (created_time > str(last_system_track_number_kirim_datetime[ix])):
                # kirimkan data dengan created time terbaru
                # dan simpan ke last_system_track_number_kirim
                last_system_track_number_kirim_datetime[ix] = created_time

            if (ar_mandatory_table_8[ix] == 'replay_system_track_general'):

                q = "SELECT system_track_number,created_time,identity,environment,source,track_name,iu_indicator,airborne_indicator  FROM ";
                q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    session_id) + " AND system_track_number = " + str(system_track_number);
                q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                cur.execute(q)
                for row in cur.fetchall():
                    results.append(dict(zip(columns, row)))
                hasil = json.dumps(results, indent=2, default=str)

            if (ar_mandatory_table_8[ix] == 'replay_system_track_kinetic'):
                q = "SELECT latitude,longitude,speed_over_ground,course_over_ground FROM ";
                q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    session_id) + " AND system_track_number = " + str(system_track_number);
                q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                cur.execute(q)
                for row in cur.fetchall():
                    results[len(results) - 1]['latitude'] = row[0]
                    results[len(results) - 1]['longitude'] = row[1]
                    results[len(results) - 1]['speed_over_ground'] = row[2]
                    results[len(results) - 1]['course_over_ground'] = row[3]

                hasil = json.dumps(results, indent=2, default=str)

            if (ar_mandatory_table_8[ix] == 'replay_system_track_processing'):
                q = "SELECT track_join_status,track_fusion_status,track_phase_type as track_phase  FROM ";
                q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    session_id) + " AND system_track_number = " + str(system_track_number);
                q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                cur.execute(q)
                for row in cur.fetchall():
                    results[len(results) - 1]['track_join_status'] = row[0]
                    results[len(results) - 1]['track_fusion_status'] = row[1]
                    results[len(results) - 1]['track_phase'] = row[2]

                hasil = json.dumps(results, indent=2, default=str)

            if (ar_mandatory_table_8[ix] == 'replay_ais_data'):
                icek_ais = 0
                if (last_system_track_number_kirim_datetime[ix] != 'None'):
                    q = "SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                    q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                        session_id) + " AND system_track_number = " + str(system_track_number);
                    q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";

                    cur.execute(q)
                    for row in cur.fetchall():
                        results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
                        results[len(results) - 1]['ship_name'] = row[1]
                        icek_ais = 1

                else:
                    q = "SELECT * FROM (SELECT type_of_ship_or_cargo,name as ship_name FROM ";
                    q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                        session_id) + " AND system_track_number = " + str(system_track_number);
                    q = q + " ORDER BY created_time DESC ) aa LIMIT 1";

                    cur.execute(q)
                    for row in cur.fetchall():
                        results[len(results) - 1]['type_of_ship_or_cargo'] = row[0]
                        results[len(results) - 1]['ship_name'] = row[1]
                        icek_ais = 1

                if (icek_ais == 0):
                    results[len(results) - 1]['type_of_ship_or_cargo'] = '-'
                    results[len(results) - 1]['ship_name'] = '-'
                print(q)
                hasil = json.dumps(results, indent=2, default=str)

            if (ar_mandatory_table_8[ix] == 'replay_track_general_setting'):
                q = "SELECT track_visibility FROM ";
                q = q + ar_mandatory_table_8[ix] + " WHERE session_id = " + str(
                    session_id) + " AND system_track_number = " + str(system_track_number);
                q = q + " AND created_time = '" + last_system_track_number_kirim_datetime[ix] + "'";
                cur.execute(q)
                for row in cur.fetchall():
                    results[len(results) - 1]['track_visibility'] = row[0]

                hasil = json.dumps(results, indent=2, default=str)

        print('-------------------------------')
        print(hasil)
        # print(system_track_number)
        # print(last_system_track_number_kirim_datetime)
except psycopg2.Error as e:
    pass
cur.close()


