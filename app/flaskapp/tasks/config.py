API_KEY = '[Ключ API Росминздрава]'
TABLE_SUFFIX_NEW = '_new'
TABLE_SUFFIX_OLD = '_old'
ROWS_PER_PAGE = 25
db_nsi = {
    'host': 'db',
    'user': 'root',
    'password': 'ChangeMe_2023',
    'charset': 'utf8',
    'database': 'nsi'
}

db_mm = {
    'host': '[Хост БД тестового контура]',
    'user': '[Пользователь БД тестового контура]',
    'password': '[Пароль пользователя БД тестового контура]',
    'database': '[Имя БД тестового контура]',
    'charset': 'utf8'
}

db_mm_master = {
    'host': '[Хост боевой БД]',
    'user': '[Пользователь боевой БД]',
    'password': '[Пароль пользователя боевой БД]',
    'database': '[Имя боевой БД]',
    'charset': 'utf8'
}

db_nsi_url = f'mysql+pymysql://{db_nsi["user"]}:{db_nsi["password"]}@{db_nsi["host"]}:3306/{db_nsi["database"]}'
db_mm_url = f'mysql+pymysql://{db_mm["user"]}:{db_mm["password"]}@{db_mm["host"]}:3306/{db_mm["database"]}'
db_mm_master_url = f'mysql+pymysql://{db_mm_master["user"]}:{db_mm_master["password"]}@{db_mm_master["host"]}:3306/{db_mm_master["database"]}'

master_mode = False

excluded_char = {'\\': r'\\',
                 '"': r'\"',
                 "'": r"\'",
                 '(': '',
                 ')': '',
                 '%': '\%',
                 '_': '\_'}
nsi_get_step = 1000

BITRIX_API_DATA = {'protocol': 'https', 'domain': '[URL Битрикс24]',
                   'auth_key': '[Ключ веб-хука Битрикс24]',
                   'user_id': '[ID пользователя от которого отправляется сообщение в чат]', 'method': 'im.message.add'}
BITRIX_API_DATA['url'] = f'rest/{BITRIX_API_DATA["user_id"]}/{BITRIX_API_DATA["auth_key"]}/{BITRIX_API_DATA["method"]}'
BITRIX_API_DATA['dialog_id'] = '[ID чата Битрикс24, куда отправляются уведомления]'
BITRIX_API_DATA['api_data'] = {'DIALOG_ID': BITRIX_API_DATA['dialog_id'],
                               'MESSAGE': '',
                               'SYSTEM': 'N',
                               'ATTACH': {'ID': 1,
                                         'COLOR': "#000000",
                                         'BLOCKS': [
                                                    {'MESSAGE': ''},
                                                    {'LINK': {
                                                                'NAME': "",
                                                                'DESC': "",
                                                                'LINK': "",
                                                              }
                                                    },

                                         ]},
                               'URL_PREVIEW': 'Y',
                               'KEYBOARD': '',
                               'MENU': '',}
