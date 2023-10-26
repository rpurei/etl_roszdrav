from sqlalchemy import text
from config import excluded_char
from datetime import datetime, timezone, timedelta

tzinfo = timezone(timedelta(hours=3.0))

# функция экранирования символов для текстовых полей БД по словарю excluded_char в config.py
def string_cleaner(str_to_clean):
    result = str_to_clean
    for char in excluded_char.keys():
        result = result.replace(char, excluded_char[char])
    return result


def db_log(session_id, table_id, status, message, query_type, operation_type, db_engine):
    try:
        if query_type == 'insert' or query_type == 'compare':
            with db_engine.connect() as conn:
                conn.execute(text(f"""INSERT INTO nsi_tables_status (SESSION_ID,OPER_START,
                                                                     OPER_TYPE, 
                                                                     TABLE_ID,
                                                                     OPER_STATUS,
                                                                     OPER_DESC) 
                                      VALUES ('{session_id}','{datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")}',
                                            '{operation_type}','{table_id}','{status}','{string_cleaner(message)}')"""))
        elif query_type == 'update' or query_type == 'complete':
            with db_engine.connect() as conn:
                result = conn.execute(text(f"""SELECT OPER_STATUS FROM nsi_tables_status 
                                               WHERE SESSION_ID=\'{session_id}\' AND TABLE_ID=\'{table_id}\'"""))
                for status_nsi in result:
                    if status_nsi:
                        if status_nsi[0] == 'Critical' or status_nsi[0] == 'Warning':
                            conn.execute(text(f"""UPDATE nsi_tables_status SET 
                                                  OPER_DESC=CONCAT(OPER_DESC,'</br>',\'{string_cleaner(message)}\') 
                                                  WHERE SESSION_ID=\'{session_id}\' 
                                                  AND TABLE_ID=\'{table_id}\' 
                                                  AND OPER_TYPE=\'{operation_type}\'"""))
                        else:
                            conn.execute(text(f"""UPDATE nsi_tables_status SET OPER_STATUS=\'{status}\',
                                                  OPER_DESC=CONCAT(OPER_DESC,'</br>',\'{string_cleaner(message)}\') 
                                                  WHERE SESSION_ID=\'{session_id}\' 
                                                  AND TABLE_ID=\'{table_id}\' 
                                                 AND OPER_TYPE=\'{operation_type}\'"""))
                if query_type == 'complete':
                    conn.execute(text(f"""UPDATE nsi_tables_status SET 
                                          OPER_END=\'{datetime.now(tzinfo).strftime("%Y-%m-%d %H:%M:%S")}\' 
                                          WHERE SESSION_ID=\'{session_id}\' 
                                          AND TABLE_ID=\'{table_id}\' 
                                          AND OPER_TYPE=\'{operation_type}\'"""))
    except Exception as err:
        raise err
