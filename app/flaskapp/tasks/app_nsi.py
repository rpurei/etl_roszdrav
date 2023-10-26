from sys import stdout
from config import *
from tables import *
from logger import db_log
import logging
from time import sleep
from pathlib import Path
from requests import post, get
from json import loads
from sqlalchemy import create_engine, text
from sqlalchemy import exc, insert, select
from sqlalchemy.dialects.mysql import insert as upsert
from sqlalchemy_utils import database_exists, create_database
from pandas import DataFrame
from argparse import ArgumentParser, ArgumentError
from hashlib import md5
from inspect import stack
from copy import deepcopy
from datetime import datetime, timezone, timedelta


def local_tz_time():
    tz_info = timezone(timedelta(hours=3.0))
    n = datetime.now(tz_info)
    return n.timetuple()


tzinfo = timezone(timedelta(hours=3.0))
now = datetime.now(tzinfo)
session_id = md5(now.strftime('%d.%m.%Y-%H:%M:%S').encode('utf-8')).hexdigest()
nsi_log_file_name = 'nsi-{}'.format(now.strftime('%d-%m-%Y-%H-%M-%S'))
Path('logs').mkdir(parents=True, exist_ok=True)
logging.Formatter.converter = local_tz_time
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s:(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
                    level=logging.INFO, datefmt='%d.%m.%Y-%H:%M:%S',
                    handlers=[logging.FileHandler(f'logs/{nsi_log_file_name + ".log"}'),
                              logging.StreamHandler(stdout)])


database_nsi_engine = create_engine(db_nsi_url, echo=False)
database_mm_engine = create_engine(db_mm_url, echo=False)
database_mm_master_engine = create_engine(db_mm_master_url, echo=False)


# отправка уведомлений в чат Битрикс, message_list - список сообщений:
# 0 - заголовок сообщения,
# 1 - тело сообщения при типе блока MESSAGE (type='message'), описание при типе блока LINK (type='link')
# 2 - имя ссылки при типе блока LINK (type='link')
# 3 - адрес ссылки при типе блока LINK (type='link')
def bitrix24_chat_send(config_dict, status, attach_type, message_list=('', '', '', '')):
    config_dict['api_data']['MESSAGE'] = message_list[0]
    if status == 'success':
        config_dict['api_data']['ATTACH']['COLOR'] = '#26940D'
    elif status == 'warning':
        config_dict['api_data']['ATTACH']['COLOR'] = '#EBD009'
    elif status == 'critical':
        config_dict['api_data']['ATTACH']['COLOR'] = '#CF1515'
    if attach_type == 'message':
        config_dict['api_data']['ATTACH']['BLOCKS'][0]['MESSAGE'] = message_list[1]
    elif attach_type == 'link':
        config_dict['api_data']['ATTACH']['BLOCKS'][1]['LINK']['NAME'] = message_list[2]
        config_dict['api_data']['ATTACH']['BLOCKS'][1]['LINK']['DESC'] = message_list[1]
        config_dict['api_data']['ATTACH']['BLOCKS'][1]['LINK']['LINK'] = message_list[3]
    resource_url = f'{config_dict["protocol"]}://{config_dict["domain"]}/{config_dict["url"]}'
    response = post(resource_url, json=config_dict['api_data'], verify=True)
    if response.status_code != 200:
        return response.json()
    else:
        return 200


# функция сложения хешей MD5 по модулю 256
def md5sum(string_source, string_to_add):
    n = 2
    hash_len = 32
    result_list = []
    hex_list_two = [0]*hash_len
    if len(string_source) == hash_len:
        hex_list_one = [int('0x' + string_source[i:i + n], 16) for i in range(0, len(string_source), n)]
        if len(string_to_add) == hash_len:
            hex_list_two = [int('0x' + string_to_add[i:i + n], 16) for i in range(0, len(string_to_add), n)]
        for index in range(0, hash_len//2):
            value = hex((hex_list_one[index] + hex_list_two[index]) % 256)[2:]
            value = value if len(value) == 2 else '0' + value
            result_list.append(value)
        return ''.join(result_list)
    else:
        return -1


# функция формирования словаря исходя из аргументов приложения
def dict_list(tables_list, config_list):
    local_config = []
    if 'all' in tables_list:
        logging.info('Processing all dictionaries')
        local_config = config_list
    else:
        logging.info(f'Processing dictionaries: \'{",".join(tables_list)}\'')
        for table in tables_list:
            for row in config_list:
                if table in row:
                    local_config.append(row)
    return local_config


# функция чтения конфига из БД НСИ
def read_config():
    try:
        with database_nsi_engine.connect() as conn:
            result = conn.execute(select(nsi_tables_config))
            config_list = [tuple(row) for row in result]
    except exc.OperationalError as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {e.args[0]}')
        raise exc.OperationalError
    return config_list


# фунция инициализации БД НСИ
def db_nsi_init():
    global database_nsi_engine
    try:
        result = database_exists(database_nsi_engine.url)
    except exc.OperationalError as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {e.args[0]}')
        raise exc.OperationalError
    else:
        if not result:
            try:
                create_database(database_nsi_engine.url, encoding=db_nsi["charset"])
                nsi_tables_config.create(database_nsi_engine, checkfirst=True)
                nsi_tables_status.create(database_nsi_engine, checkfirst=True)
                with database_nsi_engine.connect() as conn:
                    conn.execute(insert(nsi_tables_config), initial_data)
            except exc.OperationalError as e:
                logging.critical(f'In function \'{stack()[0][3]}\' error: {e.args[0]}')
                raise exc.OperationalError
        return read_config()


# манипуляция с таблицей НСИ перед обновлением - дроп _new таблицы, если такая осталась, создание _new таблицы
# из текущей таблицы
def table_preprocessing_nsi(table_name):
    old_table = table_name + TABLE_SUFFIX_OLD
    try:
        with database_nsi_engine.connect() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS {old_table}'))
            result = conn.execute(text(f'SHOW TABLES LIKE \'{table_name}\''))
            for _ in result:
                conn.execute(text(f'RENAME TABLE {table_name} TO {old_table}'))
    except Exception as e:
        raise e


# манипуляция с таблицей ММ перед обновлением - дроп _new таблицы, если такая осталась, создание _new таблицы
# из текущей таблицы
def table_preprocessing_mm(table_name):
    new_table = table_name + TABLE_SUFFIX_NEW
    try:
        with database_mm_engine.connect() as conn:
            conn.execute(text(f'DROP TABLE IF EXISTS {new_table}'))
            result = conn.execute(text(f'SHOW TABLES LIKE \'{table_name}\''))
            for _ in result:
                conn.execute(text(f'CREATE TABLE {new_table} LIKE {table_name}'))
                conn.execute(text(f'INSERT INTO {new_table} SELECT * FROM {table_name}'))
    except Exception as e:
        raise e
    else:
        return new_table


# манипуляция с таблицей ММ после обновления - дроп _old таблицы, переименование текущей таблицы в _old и
# переименование _new таблицы в текущую
def table_postprocessing_mm(table_name):
    old_table = table_name + TABLE_SUFFIX_OLD
    new_table = table_name + TABLE_SUFFIX_NEW
    try:
        with database_mm_engine.connect() as conn:
            if table_name == 'b_hlbd_insurance_companies':
                insurance_table_finish()
            elif table_name == 'b_hlbd_dictionary_departments_cabinets':
                conn.execute(text(f'UPDATE {new_table} SET UF_OID_DESK_MD5=MD5(UF_OID_DESK) WHERE 1'))
            conn.execute(text(f'DROP TABLE IF EXISTS {old_table}'))
            conn.execute(text(f'RENAME TABLE {table_name} TO {old_table}'))
            conn.execute(text(f'RENAME TABLE {new_table} TO {table_name}'))
    except Exception as e:
        raise e


# функция отката обновления, ищет для указанной таблицы _old таблицу, если не находит - пропускает, если находит -
# дропает указанную таблицу, _old таблицу переименовывает
def rollback(tables_list, db_case='mm'):
    try:
        config_list = dict_list(tables_list, read_config())
        rollback_table = None
        rollback_connect = None
        for table in config_list:
            if db_case == 'nsi':
                rollback_table = table[1]
                rollback_connect = database_nsi_engine.connect()
            elif db_case == 'mm':
                rollback_table = table[3]
                rollback_connect = database_mm_engine.connect()
            with rollback_connect as conn:
                result = conn.execute(text(f'SHOW TABLES LIKE \'{rollback_table + TABLE_SUFFIX_OLD}\''))
                for _ in result:
                    conn.execute(text(f'DROP TABLE IF EXISTS {rollback_table}'))
                    conn.execute(text(f'RENAME TABLE {rollback_table + TABLE_SUFFIX_OLD} TO {rollback_table}'))
                    logging.info(f'Rolling back for table: {rollback_table}')
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


# фукнция обновления таблиц
def common_table_update(mm_table, update_dict, renamed_dict):
    try:
        with database_mm_engine.connect() as conn_mm:
            new_table = deepcopy(globals()[mm_table])
            new_table.name = mm_table + TABLE_SUFFIX_NEW
            insert_stmt = upsert(new_table).values(renamed_dict)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(renamed_dict)
            conn_mm.execute(on_duplicate_key_stmt)
            # result = conn_mm.execute(select(new_table).where(getattr(new_table.columns,
            #                                                                    list(update_dict.items())[0][0]) ==
            #                                                                    list(update_dict.items())[0][1]))
            # count = 0
            # for _ in result:
            #     count += 1
            # if count > 0:
            #     conn_mm.execute(update(new_table).where(getattr(new_table.columns,
            #                                                       list(update_dict.items())[0][0]) ==
            #                                                       list(update_dict.items())[0][1]).values(renamed_dict))
            # else:
            #     conn_mm.execute(insert(new_table).values(renamed_dict))
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


def insurance_table_update(mm_table, update_dict, renamed_dict):
    try:
        common_table_update(mm_table, update_dict, renamed_dict)
        with database_mm_engine.connect() as conn_mm:
            conn_mm.execute(text(f"""UPDATE {mm_table} 
                                     SET UF_ERM_INSURANC_NAME=UF_NAM_SMOK 
                                     WHERE {list(update_dict.items())[0][0]}={list(update_dict.items())[0][1]}"""))
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


def insurance_table_finish():
    try:
        with database_nsi_engine.connect() as conn_nsi:
            result = conn_nsi.execute(text(f"""SELECT DISTINCT SMOCOD 
                                               FROM nsi_insurance_companies 
                                               WHERE SMOCOD IS NOT NULL"""))
            comp_list = ','.join([row[0] for row in result])
        with database_mm_engine.connect() as conn_mm:
            conn_mm.execute(text(f"""UPDATE b_hlbd_insurance_companies 
                                     SET UF_ACTIVE=0 
                                     WHERE UF_SMOCOD NOT IN ({comp_list}) AND UF_ACTIVE=1"""))
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


def units_table_update(mm_table, update_dict, renamed_dict):
    try:
        with database_mm_engine.connect() as conn_mm:
            result = conn_mm.execute(text(f"""SELECT * 
                                              FROM {mm_table} 
                                              WHERE {list(update_dict.items())[0][0]}={list(update_dict.items())[0][1]} 
                                              AND UF_SOURCE=2 OR UF_SOURCE=2"""))
            count = 0
            for _ in result:
                count += 1
            if count == 0:
                common_table_update(mm_table, update_dict, renamed_dict)
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


def departments_table_update(mm_table, update_dict, renamed_dict):
    try:
        with database_mm_engine.connect() as conn_mm:
            result = conn_mm.execute(text(f"""SELECT UF_MD5 
                                              FROM {mm_table} 
                                              WHERE {list(update_dict.items())[0][0]}=\'{list(update_dict.items())[0][1]}\'"""))
            count = 0
            for row in result:
                if row[0] == renamed_dict['UF_MD5']:
                    count += 1
            if count == 0:
                new_table = deepcopy(globals()[mm_table])
                new_table.name = mm_table + TABLE_SUFFIX_NEW
                insert_stmt = upsert(new_table).values(renamed_dict)
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(renamed_dict)
                conn_mm.execute(on_duplicate_key_stmt)
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')


def medschools_update(mm_table, update_dict, renamed_dict):
    pass


def mmdb_check(tables_list, notification):
    difference_names_list = []
    difference_tables_list = []
    try:
        config_list = dict_list(tables_list, read_config())
        tables_len = len(config_list)
        table_counter = 1
        for table in config_list:
            nsi_table = table[1]
            mm_table = table[3]
            column_match_dict = table[5]
            table_name = table[4]
            table_id = table[0]
            if nsi_table != 'nsi_medical_schools_extended':
                with database_nsi_engine.connect() as conn_nsi:
                    logging.info(f'({str(table_counter)}/{str(tables_len)}) Processing table {nsi_table} ...')
                    rows_counter = 0
                    for res in conn_nsi.execute(text(f'SELECT COUNT(*) FROM {nsi_table}')):
                        rows_counter = res[0]
                    limit = 100
                    offset = rows_counter // limit + 1
                    result_hash_nsi = ''
                    for step in range(0, offset):
                        column_list = [f'{nsi_table}.' + col for col in dict(pickle.loads(column_match_dict)).values()]
                        result = conn_nsi.execute(text(f"""SELECT MD5(CONCAT_WS(\'-\',{",".join(column_list)})) 
                                                           FROM {nsi_table} LIMIT {limit} OFFSET {step * limit}"""))
                        table_nsi_data = [row[0] for row in result]
                        for item in table_nsi_data:
                            result_hash_nsi = md5sum(item, result_hash_nsi)
                with database_mm_engine.connect() as conn_mm:
                    logging.info(f'Processing table {mm_table} ...')
                    rows_counter = 0
                    for res in conn_mm.execute(text(f'SELECT COUNT(*) FROM {mm_table}')):
                        rows_counter = res[0]
                    limit = 100
                    offset = rows_counter // limit + 1
                    result_hash_mmdb = ''
                    for step in range(0, offset):
                        result = conn_mm.execute(text(f"""SELECT MD5(CONCAT_WS(\'-\',{",".join(dict(pickle.loads(column_match_dict)).keys())})) 
                                                          FROM {mm_table} LIMIT {limit} OFFSET {step * limit}"""))
                        table_mmdb_data = [row[0] for row in result]
                        for item in table_mmdb_data:
                            result_hash_mmdb = md5sum(item, result_hash_mmdb)
                table_counter += 1
                if result_hash_nsi != result_hash_mmdb:
                    difference_names_list.append(table_name)
                    difference_tables_list.append(mm_table)
                    db_log(session_id, table_id, 'Critical', f'Таблицы неэквивалентны:</br>хэш {nsi_table}: {result_hash_nsi}</br>хэш {mm_table}: {result_hash_mmdb}', 'insert', 'Compare',
                           database_nsi_engine)
                    logging.info(f'Tables {nsi_table} and {mm_table} not equal')
                else:
                    logging.info(f'Tables {nsi_table} and {mm_table} are equal')
                    db_log(session_id, table_id, 'Success', f'Таблицы эквивалентны', 'insert', 'Compare',
                           database_nsi_engine)
        if len(difference_names_list) > 0:
            if notification:
                bitrix24_chat_send(BITRIX_API_DATA, 'warning', 'message',
                                   ('[B]Проверка справочников[/B]',
                                    f'Справочники, отличающиеся от НСИ:{chr(10)}{chr(10).join(difference_names_list)}',
                                    '',
                                    ''))
            logging.info(f'Not equal tables list: {",".join(difference_names_list)}')
        else:
            if notification:
                bitrix24_chat_send(BITRIX_API_DATA, 'success', 'message',
                                   ('[B]Проверка справочников[/B]', f'Все справочники идентичны с НСИ:', '', ''))
            logging.info(f'All tables are equal')
    except Exception as e:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'critical', 'message',
                               ('[B]Проверка справочников[/B]', f'Ошибка: {str(e)}', '', ''))
    else:
        return difference_tables_list


def nsi_download(tables_list, start_page, notification):
    table_id = -1
    try:
        config_list = dict_list(tables_list, db_nsi_init())
        pages = total = 0
        dict_counter = 1
        exception_object = None
        dict_len = len(config_list)
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'success', 'message',
                               ('[B]Загрузка справочников[/B]', f'Начата загрузка {dict_len} справочников', '', ''))
        for table in config_list:
            nsi_table = table[1]
            dict_id = table[2]
            table_id = table[0]
            column_match_dict = table[5]
            source_string = f'https://nsi.rosminzdrav.ru/port/rest/data?userKey={API_KEY}&identifier={dict_id}&size=1'
            for attempt in range(0, 5):
                try:
                    res = get(source_string)
                    myjson = loads(res.text)
                    total = myjson.get('total')
                    pages = (total // nsi_get_step) + 1 if total is not None else 0
                    if pages > 0:
                        break
                except Exception as e:
                    exception_object = e
                sleep(10)
            if pages == 0:
                raise exception_object
            logging.info(f'For dictionary {nsi_table} founded {str(total)} entries, {str(pages)} page(s) total')
            table_preprocessing_nsi(nsi_table)
            db_log(session_id, table_id, 'Started', f'Загрузка данных начата.', 'insert', 'Download', 
                   database_nsi_engine)
            for page in range(start_page, pages + 1):
                resource_url = f'https://nsi.rosminzdrav.ru/port/rest/data?userKey={API_KEY}&identifier={dict_id}&page={str(page)}&size={nsi_get_step}'
                records_dict = None
                for attempt in range(0, 5):
                    try:
                        res = get(resource_url)
                        nsi_json = loads(res.text)
                        records_dict = nsi_json.get('list')
                        if records_dict:
                            break
                    except Exception as e:
                        exception_object = e
                    sleep(10)
                if not records_dict:
                    raise exception_object
                else:
                    result_list = []
                    for record in records_dict:
                        record_list = []
                        for column in record:
                            record_list.append(tuple(column.values()))
                        result_list.append(dict(tuple(record_list)))
                    pnd = DataFrame(result_list)
                    pnd.to_sql(nsi_table, con=database_nsi_engine, if_exists='append', index=False)
                    logging.info(f'({str(dict_counter)}/{str(dict_len)}) Loading page for table: {nsi_table} {str(page)}/{str(pages)}')
            dict_counter += 1
            db_log(session_id, table_id, 'Success', f'Загрузка данных закончена.', 'complete', 'Download',
                   database_nsi_engine)
            if nsi_table == 'nsi_departments_cabinets':
                with database_nsi_engine.connect() as conn_nsi:
                    logging.info(f'Processing table {nsi_table} MD5 keys')
                    conn_nsi.execute(text(f"""UPDATE {nsi_table} 
                                              SET depart_create_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1),
                                                  depart_modify_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1),
                                                  depart_liquidation_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1),
                                                  hospital_liquidation_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1),
                                                  building_create_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1),
                                                  building_modify_date=SUBSTRING_INDEX(depart_create_date, \'.\', 1)"""))
                    conn_nsi.execute(text(f"""UPDATE {nsi_table}
                                              SET depart_create_date=REPLACE(depart_create_date, \'T\', \' \'),
                                                  depart_modify_date=REPLACE(depart_create_date, \'T\', \' \'),
                                                  depart_liquidation_date=REPLACE(depart_create_date, \'T\', \' \'),
                                                  hospital_liquidation_date=REPLACE(depart_create_date, \'T\', \' \'),
                                                  building_create_date=REPLACE(depart_create_date, \'T\', \' \'),
                                                  building_modify_date=REPLACE(depart_create_date, \'T\', \' \')"""))
                    conn_nsi.execute(text(f"""ALTER TABLE {nsi_table} 
                                              ADD UF_OID_DESK_MD5 CHAR(32) NULL, 
                                              ADD UF_MD5 CHAR(32) NULL"""))
                    conn_nsi.execute(text(f"""UPDATE {nsi_table}
                                              SET UF_OID_DESK_MD5=MD5(oid),
                                                  UF_MD5=MD5(CONCAT_WS(\'-\',{",".join(list(dict(pickle.loads(column_match_dict)).values())[:-1])})) 
                                              WHERE 1"""))
    except Exception as e:
        db_log(session_id, table_id, 'Critical', f'Ошибка {str(e)}', 'update', 'Download', database_nsi_engine)
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'critical', 'message',
                               ('[B]Загрузка справочников[/B]', f'Ошибка: {str(e)}', '', ''))
        raise e
    else:
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'success', 'message',
                               ('[B]Загрузка справочников[/B]', f'Загружено справочников: {dict_counter}/{dict_len}',
                                '', ''))


def mmdb_update(tables_list, notification):
    table_id = -1
    try:
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'success', 'message',
                               ('[B]Обновление справочников[/B]', f'Начато обновление справочников', '', ''))
        config_list = dict_list(tables_list, read_config())
        tables_len = len(config_list)
        table_counter = 1
        for table in config_list:
            nsi_table = table[1]
            mm_table = table[3]
            table_id = table[0]
            column_match_dict = table[5]
            column_update_dict = table[6]
            with database_nsi_engine.connect() as conn_nsi:
                db_log(session_id, table_id, 'Started', f'Обновление данных начато.', 'insert', 'Update',
                       database_nsi_engine)
                logging.info(f'Updating table {mm_table} ({str(table_counter)}/{str(tables_len)} tables)')
                rows_counter = update_counter = 0
                new_mm_table = table_preprocessing_mm(mm_table)
                for res in conn_nsi.execute(text(f'SELECT COUNT(*) FROM {nsi_table}')):
                    rows_counter = res[0]
                limit = 100
                offset = rows_counter // limit + 1
                for step in range(0, offset):
                    result = conn_nsi.execute(text(f'SELECT * FROM {nsi_table} LIMIT {limit} OFFSET {step * limit}'))
                    for row in result:
                        update_counter += 1
                        value_dict = dict(row)
                        update_dict = {}
                        renamed_dict = {}
                        for new_column, old_column in dict(pickle.loads(column_match_dict)).items():
                            value_dict[new_column] = value_dict.pop(old_column)
                            renamed_dict[new_column] = value_dict[new_column]
                        for new_column, old_column in dict(pickle.loads(column_update_dict)).items():
                            update_dict[new_column] = value_dict.pop(old_column)
                        if new_mm_table:
                            if mm_table == 'b_hlbd_insurance_companies':
                                insurance_table_update(mm_table, update_dict, renamed_dict)
                            elif mm_table == 'b_hlbd_nsi_units':
                                units_table_update(mm_table, update_dict, renamed_dict)
                            elif mm_table == 'b_hlbd_nsi_medical_schools_extended':
                                medschools_update(mm_table, update_dict, renamed_dict)
                            elif mm_table == 'b_hlbd_dictionary_departments_cabinets':
                                departments_table_update(mm_table, update_dict, renamed_dict)
                            else:
                                common_table_update(mm_table, update_dict, renamed_dict)
                    logging.info(f"""({str(table_counter)}/{str(tables_len)}) Updating {mm_table}: {str(update_counter)}/{str(rows_counter)} rows""")
                if new_mm_table:
                    table_postprocessing_mm(mm_table)
                    table_counter += 1
                    db_log(session_id, table_id, 'Success', f'Обновление данных завершено.', 'complete', 'Update',
                           database_nsi_engine)
    except Exception as e:
        db_log(session_id, table_id, 'Critical', f'Ошибка {str(e)}', 'insert', 'Update', database_nsi_engine)
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(e)}')
        if notification:
            bitrix24_chat_send(BITRIX_API_DATA, 'critical', 'message', 
                               ('[B]Обновление справочников[/B]', f'Ошибка БД: {str(e)}', '', ''))


if __name__ == '__main__':
    arg_list = None
    parser = ArgumentParser()
    parser.add_argument("--mode", default='download', 
                        help="""Script operating mode (default: 'download'): 
                               'full' - downloads data to NSI database and updates MMDB
                               'full-diff' - downloads data to NSI database and updates MMDB only defference tables
                               'download' - downloads data to NSI database only
                               'check' - checks difference between NSI and MMDB database
                               'update-diff' - updates MMDB from NSI database only defference tables
                               'update' - updates MMDB from NSI database
                               'rollback' - !!! REMOVES tables and RENAMES *_old tables to original
                       'download-check' - downloads data to NSI and checks difference between NSI and MMDB database""")
    parser.add_argument("--tables", default='all', 
                        help="""Comma separated list(without spaces) of tables to update 
                                (default: 'all'): 'all' - downloads data to NSI database for all tables
                                for table names - check config.py, table name - key of HLBD dictionary""")
    parser.add_argument("--startpage", type=int, default=1, help="""Number of start page to download data from NSI""")
    parser.add_argument("--notify", default='no', help="""Send or not notifications to Bitrix24 chat, default: no""")
    parser.add_argument("--mastermode", default='no', help="""Work with master database, default: no""")
    try:
        arg_list = parser.parse_args()
    except ArgumentError:
        logging.critical(f'Argument parsing error {ArgumentError}, unsuccessfully exiting app (((')
        exit(-1)
    notif = True if arg_list.notify == 'yes' else False
    master_mode = True if arg_list.mastermode == 'yes' else False
    logging.info(f"""App started with arguments: 
                            mode=\'{arg_list.mode}\' 
                            tables=\'{arg_list.tables}\' 
                            start page=\'{arg_list.startpage}\' 
                            notifications=\'{arg_list.notify}\' 
                            mastermode=\'{arg_list.mastermode}\'""")
    try:
        if master_mode:
            database_mm_engine = database_mm_master_engine
            logging.info(f'App started with MASTER MODE!!!')
        if arg_list.mode == 'full':
            nsi_download(arg_list.tables.split(','), arg_list.startpage, notif)
            mmdb_update(arg_list.tables.split(','), notif)
        elif arg_list.mode == 'full-diff':
            nsi_download(arg_list.tables.split(','), arg_list.startpage, notif)
            mmdb_update(mmdb_check(arg_list.tables.split(','), notif), notif)
        elif arg_list.mode == 'download':
            nsi_download(arg_list.tables.split(','), arg_list.startpage, notif)
        elif arg_list.mode == 'check':
            mmdb_check(arg_list.tables.split(','), notif)
        elif arg_list.mode == 'update-diff':
            mmdb_update(mmdb_check(arg_list.tables.split(','), notif), notif)
        elif arg_list.mode == 'update':
            mmdb_update(arg_list.tables.split(','), notif)
        elif arg_list.mode == 'rollback':
            rollback(arg_list.tables.split(','), 'mm')
        elif arg_list.mode == 'download-check':
            nsi_download(arg_list.tables.split(','), arg_list.startpage, notif)
            mmdb_check(arg_list.tables.split(','), notif)
        elif arg_list.mode == 'init-config':
            db_nsi_init()
        else:
            logging.critical('Unrecognized mode, use --help to view available options')
    except Exception as err:
        logging.critical(f'In function \'{stack()[0][3]}\' error: {str(err)}')
