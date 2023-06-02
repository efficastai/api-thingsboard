postgres = {
    'get_ppm_day_accumulator': (
        "SELECT SUM(long_v) "
        "FROM ts_kv_{}_{} t JOIN device d "
        "ON t.entity_id = d.id "
        "WHERE date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "AND t.key = 36 AND d.name = '{}'"
    ),
    'get_ppm_week_accumulator': (
        "SELECT SUM(long_v) "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE date_trunc('week', to_timestamp(ts/1000)) = "
        "date_trunc('week', current_timestamp) "
        "AND t.key = 36 "
        "AND d.name = '{}'"
    ),
    'get_ppm_month_accumulator': (
        "SELECT SUM(long_v) "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE t.key = 36 "
        "AND d.name = '{}'"
    ),
    'get_pya_day_accumulator': (
        "SELECT SUM(long_v) "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "AND t.key = 34 "
        "AND d.name = '{}'"
    ),
    'get_ppm_count_day_accumulator': (
        "SELECT COUNT(long_v) "
        "FROM ts_kv_{}_{} t JOIN device d "
        "ON t.entity_id = d.id "
        "WHERE date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "AND t.key = 36 AND d.name = '{}' "
        "AND long_v >= 1"
    ),
    'get_ppm_last_n_values': (
        "SELECT SUM(long_v) "
        "FROM ("
        "    SELECT long_v "
        "    FROM ts_kv_{}_{} t "
        "    JOIN device d ON t.entity_id = d.id "
        "    WHERE t.key = 36 "
        "    AND d.name = '{}' "
        "    ORDER BY ts DESC LIMIT '{}'"
        ") AS last_values;"
    ),
    'get_pya_last_n_values': (
        "SELECT SUM(long_v) "
        "FROM ("
        "    SELECT long_v "
        "    FROM ts_kv_{}_{} t "
        "    JOIN device d ON t.entity_id = d.id "
        "    WHERE t.key = 34 "
        "    AND d.name = '{}' "
        "    ORDER BY ts DESC LIMIT '{}'"
        ") AS last_values;"
    ),
    'get_pya_last_n_registers_asc': (
        "SELECT ts, long_v "
        "FROM ("
        "   SELECT ts, long_v "
        "   FROM ts_kv_{}_{} t "
        "   JOIN device d ON t.entity_id = d.id "
        "   WHERE d.name = '{}' "
        "   AND t.key = 34 "
        "   ORDER BY t.ts DESC "
        "   LIMIT '{}'"
        ") AS subquery "
        "ORDER BY ts ASC"
    ),
    'get_last_data_ts': (
        "SELECT ts "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE d.name = '{}' "
        "AND t.key = 36 "
        "ORDER BY t.ts DESC "
        "LIMIT 1"
    ),
    'get_last_data_ts': (
        "SELECT ts "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE d.name = '{}' "
        "AND t.key = 36 "
        "ORDER BY t.ts DESC "
        "LIMIT 1"
    ),
    'get_day_pya_values': (
        "SELECT long_v, ts "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "AND t.key = 34 "
        "AND d.name = '{}'"
    ),
    'get_day_ppm_values': (
        "SELECT long_v, ts "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "AND t.key = 36 "
        "AND d.name = '{}'"
    ),
    'get_device_access_token': (
        "SELECT credentials_id "
        "FROM device_credentials dc "
        "JOIN device d on dc.device_id = d.id "
        "WHERE d.name = '{}'"
    ),
    'get_last_ts_where_ppm_equals_1': (
        "SELECT ts "
        "FROM ts_kv_{}_{} t "
        "JOIN device d ON t.entity_id = d.id "
        "WHERE d.name = '{}' "
        "AND t.key = 36 "
        "AND t.long_v >= 1 "
        "ORDER BY t.ts DESC "
        "OFFSET 1 "
        "LIMIT 1"
    ),
    'get_pya_total_accumulator': (
        "SELECT SUM(long_v) "
        "FROM ts_kv t JOIN device d "
        "ON t.entity_id = d.id "
        "WHERE t.key = 34 "
        "AND d.name = '{}'"
    ),
    # TENSAR QUERY
    'insert_tensar_data': (
        "INSERT INTO tensar (ts, value, dif, device, counter) "
        "VALUES({}, {}, {}, '{}', {})"
    ),
    'get_tensar_last_ts': (
        "SELECT ts "
        "FROM tensar "
        "WHERE device = '{}' "
        "ORDER BY ts DESC "
        "LIMIT 1"
    ),
    'get_tensar_day_last_register': (
        "SELECT ts, dif "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "ORDER BY ts DESC "
        "LIMIT 1"
    ),
    'get_tensar_day_last_value': (
        "SELECT ts, value "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND date_trunc('day', to_timestamp(ts/1000)) = '{}' "
        "ORDER BY ts DESC "
        "LIMIT 1"
    ),
    'update_tensar_last_value': (
        "UPDATE tensar "
        "SET value = {} , dif = {} "
        "WHERE device = '{}'"
    ),
    'count_tensar_values': (
        "SELECT COUNT(*) "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND value = {} "
        "AND date_trunc('day', to_timestamp(ts/1000)) = '{}' "
    ),
    'get_tensar_day_accumulator': (
        "SELECT COUNT(*) "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND date_trunc('day', to_timestamp(ts/1000)) = '{}'"
    ),
    'get_tensar_week_accumulator': (
        "SELECT COUNT(*) "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND date_trunc('week', to_timestamp(ts/1000)) = "
        "date_trunc('week', current_timestamp) "
    ),
    'get_tensar_month_accumulator': (
        "SELECT COUNT(*) "
        "FROM tensar "
        "WHERE device = '{}' "
        "AND date_trunc('month', to_timestamp(ts/1000)) = "
        "date_trunc('month', current_timestamp) "
    ),
    'get_tensar_last_counter': (
        "SELECT counter "
        "FROM tensar "
        "WHERE device = '{}' "
        "ORDER BY ts DESC "
        "LIMIT 1"
    )
}
