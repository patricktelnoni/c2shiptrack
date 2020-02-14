#!/usr/bin/env python

# WS server example that synchronizes REALTIME_state across clients


import psycopg2, json
from datetime import timedelta, datetime
import datetime as dt
from functools import reduce
import numpy as np
from collections import Counter

conn = psycopg2.connect("host=127.0.0.1 \
    dbname=shiptrack \
    user=postgres \
    password=1234"
)

UPDATE_RATE = 10
cur = conn.cursor()
# q = "SELECT aa.session_id as id, aa.*  FROM area_alerts aa  JOIN (    SELECT object_id,max(last_update_time) last_update_time     FROM area_alerts     WHERE session_id = '1' AND last_update_time > '2020-01-10 14:14:31' AND last_update_time < '2020-01-10 14:14:41'     GROUP BY object_id ) mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time  WHERE aa.session_id = '1'  AND aa.last_update_time > '2020-01-10 14:14:31' AND aa.last_update_time < '2020-01-10 14:14:41'  ORDER BY aa.object_id"
'''Get data session yang sudah selesai'''
sql = "select id, to_char (start_time::timestamp, 'YYYY-MM-DD HH24:MI:SS') start_time, " \
              " to_char (end_time::timestamp, 'YYYY-MM-DD HH24:MI:SS') end_time, " \
              "extract(epoch from (end_time::timestamp - start_time::timestamp)) as durasi " \
              " from sessions " \
              "WHERE end_time IS NOT null"

cur.execute(sql)
query = cur.fetchall()
track = []

def replay_track(session_id, start_time, end_time):
    track_data = []
    ar_mandatory_table_8 = [
        'replay_system_track_general',
        'replay_system_track_kinetic',
        'replay_system_track_processing',
        'replay_system_track_identification',
        'replay_system_track_link',
        'replay_system_track_mission',
        'replay_track_general_setting',
        'replay_ais_data'
    ]
    ar_mandatory_table = [
        'replay_system_track_general',
        'replay_system_track_kinetic',
        'replay_system_track_processing'
    ]

    data_lengkap = []
    for table in ar_mandatory_table:
        sql_mandatory = "SELECT st.system_track_number \
                 FROM "+table+" st \
                JOIN( \
                    SELECT system_track_number,max(created_time) created_time \
                    FROM "+table+" \
                    WHERE session_id = "+str(session_id)+" AND created_time > '"+str(start_time)+"' AND created_time < '"+str(end_time)+"' \
                    GROUP BY system_track_number \
                ) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time \
                WHERE st.session_id = "+str(session_id)+" AND st.created_time > '"+str(start_time)+"' AND st.created_time < '"+str(end_time)+"' \
                ORDER BY st.system_track_number"
        # print(sql_track)
        cur.execute(sql_mandatory)
        data = cur.fetchall()
        if len(data) > 0:            
            data_lengkap.append(data)    
    if len(data_lengkap) == 3:
        same_system_track_number  = []
        data_ready = reduce(np.intersect1d, data_lengkap)        
        for table in ar_mandatory_table_8:            
            sql_track = "SELECT st.* \
                        FROM "+table+" st \
                        JOIN( \
                            SELECT system_track_number,max(created_time) created_time \
                            FROM "+table+" \
                            WHERE session_id = "+str(session_id)+" AND created_time > '"+start_time+"' AND created_time < '"+end_time+"' \
                            GROUP BY system_track_number \
                        ) mx ON st.system_track_number=mx.system_track_number and st.created_time=mx.created_time \
                        WHERE st.session_id = "+str(session_id)+" AND st.created_time > '"+start_time+"' AND st.created_time < '"+end_time+"' \
                        ORDER BY st.system_track_number"
            # print(sql_track)
            cur.execute(sql_track)
            data = cur.fetchall()

            if table == 'replay_system_track_general' :
                # print(sql_track)
                for d in data:
                    source_data = d[10]
                    system_track_number = d[1]
                    if(source_data=='AIS_TYPE'):
                        q_ais_data = "SELECT " \
                                "   * " \
                                "FROM " \
                                "(" \
                                "   SELECT " \
                                "       type_of_ship_or_cargo," \
                                "       name as ship_name " \
                                "   FROM replay_ais_data " \
                                "   WHERE session_id = " + str(session_id) +" " \
                                "   AND system_track_number = " + str(system_track_number) +" " \
                                "   ORDER BY created_time DESC " \
                                ") aa LIMIT 1;"  
                        # print(q_ais_data)
                        cur.execute(q_ais_data)
                        data = cur.fetchall()
                        if len(data) > 0:
                            t_status = "T" + str(system_track_number)                    
                            if t_status not in track_data : 
                                track_data.append(t_status)
            else:
                for d in data:                
                    system_track_number = d[1]
                    t_status = "T" + str(system_track_number)
                    # track_table.append(t_status)
                    # print(track_table)
                    if t_status not in track_data : 
                        track_data.append(t_status)
    # duplicate   = reduce(np.intersect1d, np.array(track_list)) if len(track_list) > 0 else []
    # d           =  Counter(duplicate)  # -> Counter({4: 3, 6: 2, 3: 1, 2: 1, 5: 1, 7: 1, 8: 1})
    # track_list  = [k for k, v in d.items() if v >= 1]
    # print(start_time, ", " ,  end_time, ", ",track_data)
    return track_data



for data in query:    
    session_id  = data[0]
    start_time  = data[1]
    end_time    = data[2]
    durasi      = data[3]
    '''Buat panjang durasi dibagi dengan UPDATE_RATE. Buat list sesuai dengan panjang_replay'''
    panjang_replay = durasi / UPDATE_RATE
    track_list = [i for i in range(int(panjang_replay))]
    track_list = dict.fromkeys(track_list, "")
    result={
                    'session_id'        : session_id,
                    'update_rate'       : UPDATE_RATE,
                    'durasi_session'    : durasi,
                    'track_play'        : track_list
            }
    start_time  = (datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S'))
    end_time    = (datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S'))
    added_track = []
    '''Looping sebanyak panjang replay'''
    for t in range(len(track_list)+1):
        '''Buat start_time dan end_time untuk setiap segmen replay.
                    Segmen durasi adalah satuan  replay track, 
                    contoh 2020-01-10 14:45:31 sampai dengan 2020-01-10 14:45:41
                    disebut sebagai 1 segmen durasi'''
        
                # print(t)
                # print(str(start_time) + " sampai dengan " + str(end_time))
        if t == 0:
                tmp_time = (datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S'))
                tmp_time += dt.timedelta(seconds=UPDATE_RATE)
                end_time = tmp_time
        else:
                start_time += dt.timedelta(seconds=UPDATE_RATE)
                end_time += dt.timedelta(seconds=UPDATE_RATE)
        track_data = {
                    "start_segment" : str(start_time),
                    "end_segment"   : str(end_time),
                    "data"          : []
        }
        '''Jalankan query untuk setiap tabel per setiap segmen durasi'''

        track_replay_data = replay_track(session_id, str(start_time), str(end_time))
        track_data['data'].extend(track_replay_data)
        # track_data.append(track_replay_data)
        query_tf = "SELECT tf.* " \
                               "FROM tactical_figures tf " \
                                "JOIN(" \
                               "     SELECT object_id,max(last_update_time) last_update_time " \
                               "     FROM tactical_figures " \
                               "     WHERE session_id = " + str(session_id) + " AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
                                "     GROUP BY object_id) mx " \
                                "ON tf.object_id=mx.object_id and tf.last_update_time=mx.last_update_time " \
                                "WHERE tf.session_id = '"+str(session_id)+"' AND tf.last_update_time > '"+str(start_time)+"' AND tf.last_update_time < '"+str(end_time)+"' " \
                                "ORDER BY tf.object_id"
        
        cur.execute(query_tf)
        data_tf = cur.fetchall()        
        for tf in data_tf:
            object_id       = tf[2]
            is_visible      = tf[8]
            tf_status       = 'F'+str(object_id)
            if tf_status not in added_track:
                added_track.append(tf_status)
                tf_status = tf_status + 'A'
            else:
                if is_visible == 'REMOVE':
                    added_track.remove(tf_status)
                    tf_status_ = tf_status + 'R'                    
                else:
                    tf_status = tf_status + 'U'            
            track_data['data'].append(tf_status)

        query_rp = "SELECT rrp.* " \
                           "FROM replay_reference_point rrp \
                           JOIN (" \
                           "    SELECT object_id,max(last_update_time) last_update_time " \
                           "    FROM replay_reference_point " \
                           "    WHERE session_id = " + str(session_id) + " AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
                           "    GROUP BY object_id" \
                           ") mx ON rrp.object_id=mx.object_id and rrp.last_update_time=mx.last_update_time" \
                           " WHERE rrp.session_id = '"+str(session_id)+"' AND rrp.last_update_time > '"+str(start_time)+"' AND rrp.last_update_time < '"+str(end_time)+"' " \
                           "ORDER BY rrp.object_id"    
        cur.execute(query_rp)
        data_rp = cur.fetchall()
        
        for rp in data_rp:
            object_id = rp[2]
            visibility_type = rp[7]
            rp_status = 'P' + str(object_id) #+'R' if visibility_type == 'REMOVE' else 'P'+str(object_id)
            if rp_status not in added_track:
                added_track.append(rp_status)
                rp_status = rp_status + 'A'
            else:
                if visibility_type == 'REMOVE':
                    added_track.remove(rp_status)
                    rp_status = rp_status + 'R'                    
                else:
                    rp_status = rp_status + 'U'           
            track_data['data'].append(rp_status)

        query_aa = "SELECT aa.session_id as id, aa.* " \
                            " FROM area_alerts aa " \
                            " JOIN (" \
                            "    SELECT object_id,max(last_update_time) last_update_time " \
                            "    FROM area_alerts " \
                            "    WHERE session_id = '" + str(session_id) + "' AND last_update_time > '"+str(start_time)+"' AND last_update_time < '"+str(end_time)+"' " \
                            "    GROUP BY object_id " \
                            ") mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time " \
                            " WHERE aa.session_id = '" + str(session_id) + "' " \
                             " AND aa.last_update_time > '"+str(start_time)+"' AND aa.last_update_time < '"+str(end_time)+"' " \
                             " ORDER BY aa.object_id"
                # query_aa = "SELECT aa.session_id as id, aa.*  FROM area_alerts aa  JOIN (    SELECT object_id,max(last_update_time) last_update_time     FROM area_alerts     WHERE session_id = '1' AND last_update_time > '2020-01-10 14:14:31' AND last_update_time < '2020-01-10 14:14:41'     GROUP BY object_id ) mx ON aa.object_id=mx.object_id and aa.last_update_time=mx.last_update_time  WHERE aa.session_id = '1'  AND aa.last_update_time > '2020-01-10 14:14:31' AND aa.last_update_time < '2020-01-10 14:14:41'  ORDER BY aa.object_id"
        cur.execute(query_aa)
        data_aa = cur.fetchall()
        for aa in data_aa: 
            object_id = aa[3]
            is_visible = aa[9]           
            aa_status = 'AA' + str(object_id) #+'R' if is_visible == 'REMOVE' else 'AA'+str(object_id)
            if aa_status not in added_track:
                added_track.append(aa_status)
                aa_status = aa_status + 'A'
            else:
                if is_visible == 'REMOVE':
                    added_track.remove(aa_status)
                    aa_status = aa_status + 'R'                    
                else:
                    aa_status = aa_status + 'U' 
            
            track_data['data'].append(aa_status)

        result['track_play'][t] = track_data


    track.append(result)
# print(result[114])
print(json.dumps(result))
