from ..tasks.config import ROWS_PER_PAGE, master_mode as mm
from random import randint
from ..tasks.tasks import long_task_start
from ..models.models import database_mm_engine, database_mm_master_engine, User, Config, db_alchemy
from .forms import *
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from jinja2 import TemplateNotFound
from celery import current_app
from uuid import uuid4
from datetime import date
from sqlalchemy import select, text
from pickle import loads, dumps
from flask_paginate import Pagination, get_page_parameter
from flask_login import logout_user, current_user, login_user, login_required
from itertools import zip_longest
from hashlib import md5
from flask_login import LoginManager


view_page = Blueprint('view_page', __name__)
auth = Blueprint('auth', __name__)
login_manager = LoginManager()
verify_code = randint(10000, 99999)
master_mode = mm


@view_page.route('/runAsyncTaskF', methods=['POST'])
@login_required
def task_start():
    return long_task_start(request.form.get('task_args'))


@view_page.route('/', methods=['POST', 'GET'])
def index_show():
    try:
        if 'uid' not in session:
            sid = str(uuid4())
            session['uid'] = sid
        nsi_download_desc = None
        nsi_download_data = None
        nsi_update_data = None
        nsi_compare_data = None
        searchform = SearchForm()
        filter_date = date.today()
        filter_date_sql = f""" AND OPER_START>='{filter_date} 00:00:00'
                               AND OPER_START<='{filter_date} 23:59:59' """
        dict_name = searchform.select_dict.data
        dict_name = '' if dict_name == 'All' else f' AND MMDB_TABLE_NAME=\'{dict_name}\''
        if searchform.validate_on_submit():
            filter_date = searchform.dt.data.strftime('%Y-%m-%d') if searchform.dt.data else ''
            dict_name = searchform.select_dict.data
            dict_name = '' if dict_name == 'All' else f' AND MMDB_TABLE_NAME=\'{dict_name}\''
            filter_date_sql = f"""AND OPER_START>='{filter_date} 00:00:00'
                                  AND OPER_START<='{filter_date} 23:59:59' """ if filter_date else ''
            try:
                with database_nsi_engine.connect() as conn:
                    result_dnl = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_END,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status 
                                                       JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Download\'{filter_date_sql}{dict_name}"""))
                    nsi_download_data = [list(row) for row in result_dnl]
                    for row in nsi_download_data:
                        row[5] = f'<a href="{url_for("view_page.dict_show", select_dict=row[7])}" class="text-decoration-none">{row[5]}</a>'
                        del(row[7])
                    nsi_download_desc = ['ID', 'Сессия', 'Начало', 'Конец', 'Статус', 'Справочник', 'Данные операции']
                    result_upd = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_END,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Update\'{filter_date_sql}{dict_name}"""))
                    nsi_update_data = [list(row) for row in result_upd]
                    for row in nsi_update_data:
                        row[5] = f'<a href="{url_for("view_page.dict_show", select_dict=row[7])}" class="text-decoration-none">{row[5]}</a>'
                        del(row[7])
                    result_cmp = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status 
                                                       JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Compare\'{filter_date_sql}{dict_name}"""))
                    nsi_compare_data = [list(row) for row in result_cmp]
                    for row in nsi_compare_data:
                        row[4] = f'<a href="{url_for("view_page.compare_show", select_dict=row[6])}" class="text-decoration-none">{row[4]}</a>'
                        del(row[6])
                    nsi_compare_desc = ['ID', 'Сессия', 'Начало', 'Статус', 'Справочник', 'Данные операции']
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
        elif request.method == 'GET':
            try:
                with database_nsi_engine.connect() as conn:
                    result_dnl = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_END,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status 
                                                       JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Download\'{filter_date_sql}"""))
                    nsi_download_data = [list(row) for row in result_dnl]
                    for row in nsi_download_data:
                        row[
                            5] = f'<a href="{url_for("view_page.dict_show", select_dict=row[7])}" class="text-decoration-none">{row[5]}</a>'
                        del (row[7])
                    nsi_download_desc = ['ID', 'Сессия', 'Начало', 'Конец', 'Статус', 'Справочник', 'Данные операции']
                    result_upd = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_END,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status 
                                                       JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Update\'{filter_date_sql}"""))
                    nsi_update_data = [list(row) for row in result_upd]
                    for row in nsi_update_data:
                        row[
                            5] = f'<a href="{url_for("view_page.dict_show", select_dict=row[7])}" class="text-decoration-none">{row[5]}</a>'
                        del (row[7])
                    result_cmp = conn.execute(text(f"""SELECT nsi_tables_status.ID,
                                                              SESSION_ID,
                                                              OPER_START,
                                                              OPER_STATUS,
                                                              DICT_NAME,
                                                              OPER_DESC,
                                                              MMDB_TABLE_NAME 
                                                       FROM nsi_tables_status 
                                                       JOIN nsi_tables_config 
                                                       ON nsi_tables_status.TABLE_ID=nsi_tables_config.ID 
                                                       WHERE OPER_TYPE = \'Compare\'{filter_date_sql}"""))
                    nsi_compare_data = [list(row) for row in result_cmp]
                    for row in nsi_compare_data:
                        row[4] = f'<a href="{url_for("view_page.compare_show", select_dict=row[6])}" class="text-decoration-none">{row[4]}</a>'
                        del (row[6])
                    nsi_compare_desc = ['ID', 'Сессия', 'Начало', 'Статус', 'Справочник', 'Данные операции']
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
        login = ''
        if current_user.is_authenticated:
            login=current_user.name
        return render_template(f'index.html', master_mode=master_mode, table_download_desc=nsi_download_desc,
                               table_download_data=nsi_download_data, table_update_data=nsi_update_data,
                               table_compare_data=nsi_compare_data, table_compare_desc=nsi_compare_desc,
                               form_search=searchform, login=login)
    except TemplateNotFound:
        return render_template(f'404.html')


@view_page.route('/operations', methods=['POST', 'GET'])
@login_required
def operations_show():
    try:
        process_form = ProcessDictionariesForm(task_start='stop', master_mode=master_mode)
        dict_labels_mz = []
        dict_labels_mm = []
        try:
            with database_nsi_engine.connect() as conn:
                result = conn.execute(select(nsi_tables_config))
                for row in result:
                    row_tuple = tuple(row)
                    dict_labels_mz.append(f'<a href="https://nsi.rosminzdrav.ru/#!/refbook/{row_tuple[2]}" class="text-decoration-none">Данные МЗ РФ</a>')
                    dict_labels_mm.append(f'<a href="{url_for("view_page.dict_show", select_dict=row_tuple[3])}" class="text-decoration-none">Данные Medmap</a>')
        except Exception as err:
            flash(str(err), 'danger')
        celery_worker = current_app.control.inspect()
        celery_dict = celery_worker.active()
        task_id = ''
        submit_disable = ''
        stop_disable = 'none'
        if not celery_dict:
            flash('Нет соединения с Celery', 'danger')
        else:
            if len(list(celery_dict.values())[0]) > 0:
                task_id = list(celery_dict.values())[0][0]['id']
                process_form.task_id.data = task_id
                submit_disable = 'disabled'
                stop_disable = 'block'
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('operations.html', master_mode=master_mode, dict_labels_mz=dict_labels_mz,
                               dict_labels_mm=dict_labels_mm, process_form=process_form, tasks=task_id,
                               submit_disable=submit_disable, stop_disable=stop_disable, login=login)
    except TemplateNotFound:
        return render_template(f'404.html')


@view_page.route('/stop', methods=['POST'])
@login_required
def operations_stop():
    celery_worker = current_app.control.inspect()
    celery_dict = celery_worker.active()
    current_app.control.revoke(list(celery_dict.values())[0][0]['id'], terminate=True)
    flash(f'Задание {list(celery_dict.values())[0][0]["id"]} остановлено', 'info')
    return redirect(url_for('view_page.operations_show'))


@view_page.route('/config', methods=['POST', 'GET'])
@login_required
def config_show():
    global master_mode
    masterform = MasterAccessForm(code=verify_code)
    try:
        table_config_data = []
        table_config_desc = []
        try:
            with database_nsi_engine.connect() as conn:
                result = conn.execute(select(nsi_tables_config))
                for row in result:
                    row_tuple = list(row)
                    row_tuple[5] = loads(row_tuple[5]) if row_tuple[5] else None
                    row_tuple[6] = loads(row_tuple[6]) if row_tuple[6] else None
                    row_tuple[7] = loads(row_tuple[7]) if row_tuple[7] else None
                    row_tuple[8] = loads(row_tuple[8]) if row_tuple[8] else None
                    table_config_data.append(row_tuple)
                table_config_desc = ['ID', 'Имя таблицы НСИ', 'OID справочника', 'Имя таблицы ММ',
                                     'Название', 'Соответствие полей', 'Ключ', 'Преобразование', 'Доп.параметры', '']
        except Exception as err:
            #current_app.logger.error(str(err))
            flash(f'Ошибка: {str(err)}', 'danger')
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        if masterform.validate_on_submit():
            if int(masterform.code.data) == int(masterform.confirm.data):
                master_mode = True
            else:
                master_mode = False
        return render_template('config.html', master_mode=master_mode, master_form=masterform,
                               table_config_desc=table_config_desc, table_config_data=table_config_data, login=login)
    except TemplateNotFound:
        return render_template(f'404.html')


@view_page.route('/masterdisable', methods=['POST'])
@login_required
def config_disable():
    global master_mode
    master_mode = False
    global verify_code
    verify_code = randint(10000, 99999)
    return redirect(url_for('view_page.config_show'))


@view_page.route('/config/edit/<int:record_id>', methods=['GET', 'POST'])
@login_required
def config_edit(record_id):
    form_config_edit = None
    table_name = ''
    table_config_desc = ['Имя таблицы НСИ', 'OID справочника', 'Имя таблицы ММ', 'Название', 'Соответствие полей',
                         'Ключ', 'Преобразование', 'Доп.параметры', 'Операции']
    config_item = None
    try:
        config_item = Config.query.get_or_404(record_id)
        config_item.COLUMN_MATCHING = loads(config_item.COLUMN_MATCHING) if config_item.COLUMN_MATCHING else ''
        config_item.COLUMN_UPDATE = loads(config_item.COLUMN_UPDATE) if config_item.COLUMN_UPDATE else ''
        config_item.COLUMN_CONVERT = loads(config_item.COLUMN_CONVERT) if config_item.COLUMN_CONVERT else ''
        config_item.COLUMN_EXTRA = loads(config_item.COLUMN_EXTRA) if config_item.COLUMN_EXTRA else ''
        table_name = config_item.DICT_NAME
        form_config_edit = ConfigEditForm(obj=config_item)
    except Exception as err:
        flash(f'Ошибка: {str(err)}', 'danger')
    if form_config_edit.validate_on_submit():
        if request.form.get('action') == 'cancel':
            return redirect(url_for('view_page.config_show'))
        elif request.form.get('action') == 'confirm':
            try:
                config_item = Config.query.get_or_404(record_id)
                config_item.NSI_TABLE_NAME = form_config_edit.NSI_TABLE_NAME.data
                config_item.OID = form_config_edit.OID.data
                config_item.MMDB_TABLE_NAME = form_config_edit.MMDB_TABLE_NAME.data
                config_item.DICT_NAME = form_config_edit.DICT_NAME.data
                config_item.COLUMN_MATCHING = dumps(eval(form_config_edit.COLUMN_MATCHING.data)) if form_config_edit.COLUMN_MATCHING.data else None
                config_item.COLUMN_UPDATE = dumps(eval(form_config_edit.COLUMN_UPDATE.data)) if form_config_edit.COLUMN_UPDATE.data else None
                config_item.COLUMN_CONVERT = dumps(eval(form_config_edit.COLUMN_CONVERT.data)) if form_config_edit.COLUMN_CONVERT.data else None
                config_item.COLUMN_EXTRA = dumps(eval(form_config_edit.COLUMN_EXTRA.data)) if form_config_edit.COLUMN_EXTRA.data else None
                db_alchemy.session.commit()
                flash(f'Данные конфигурации справочника {config_item.DICT_NAME} обновлены', 'success')
                return redirect(url_for('view_page.config_show'))
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
    elif request.method == 'GET':
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('config_edit.html', master_mode=master_mode,
                               table_config_desc=table_config_desc, table_config_data=config_item,
                               form_config_edit=form_config_edit, table_name=table_name, login=login)


@view_page.route('/config/delete/<int:record_id>', methods=['GET', 'POST'])
@login_required
def config_delete(record_id):
    form_config_delete = ConfigDeleteForm()
    config_item = Config.query.get_or_404(record_id)
    form_config_delete.ID = config_item.ID
    form_config_delete.DICT_NAME = config_item.DICT_NAME
    if form_config_delete.validate_on_submit():
        if request.form.get('action') == 'cancel':
            return redirect(url_for('view_page.config_show'))
        elif request.form.get('action') == 'confirm':
            try:
                config_item = Config.query.get_or_404(record_id)
                db_alchemy.session.delete(config_item)
                db_alchemy.session.commit()
                flash(f'Данные конфигурации справочника {config_item.DICT_NAME} удалены', 'success')
                return redirect(url_for('view_page.config_show'))
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
    elif request.method == 'GET':
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('config_delete.html', master_mode=master_mode,
                               form_config_delete=form_config_delete, table_name=config_item.DICT_NAME, login=login)


@view_page.route('/config/add', methods=['GET', 'POST'])
@login_required
def config_add():
    form_config_add = ConfigEditForm()
    table_config_desc = ['Имя таблицы НСИ', 'OID справочника', 'Имя таблицы ММ', 'Название', 'Соответствие полей',
                         'Ключ', 'Преобразование', 'Доп.параметры', 'Операции']
    if form_config_add.validate_on_submit():
        if request.form.get('action') == 'cancel':
            return redirect(url_for('view_page.config_show'))
        elif request.form.get('action') == 'confirm':
            config_item = Config()
            config_item.NSI_TABLE_NAME = form_config_add.NSI_TABLE_NAME.data
            config_item.OID = form_config_add.OID.data
            config_item.MMDB_TABLE_NAME = form_config_add.MMDB_TABLE_NAME.data
            config_item.DICT_NAME = form_config_add.DICT_NAME.data
            config_item.COLUMN_MATCHING = dumps(eval(form_config_add.COLUMN_MATCHING.data)) if form_config_add.COLUMN_MATCHING.data else None
            config_item.COLUMN_UPDATE = dumps(eval(form_config_add.COLUMN_UPDATE.data)) if form_config_add.COLUMN_UPDATE.data else None
            config_item.COLUMN_CONVERT = dumps(eval(form_config_add.COLUMN_CONVERT.data)) if form_config_add.COLUMN_CONVERT.data else None
            config_item.COLUMN_EXTRA = dumps(eval(form_config_add.COLUMN_EXTRA.data)) if form_config_add.COLUMN_EXTRA.data else None
            try:
                db_alchemy.session.add(config_item)
                db_alchemy.session.commit()
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
            else:
                flash(f'Данные конфигурации справочника {config_item.DICT_NAME} добавлены', 'success')
            return redirect(url_for('view_page.config_show'))
    elif request.method == 'GET':
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('config_add.html', master_mode=master_mode, form_config_add=form_config_add,
                               table_config_desc=table_config_desc, login=login)


@view_page.route('/dicts')
@login_required
def dict_show():
    try:
        if master_mode:
            database_engine = database_mm_master_engine
        else:
            database_engine = database_mm_engine
        dict_name = request.args.get('select_dict', default='', type=str)
        dict_form = DictForm(select_dict=dict_name)
        table_desc = []
        table_data = []
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start_at = (page - 1) * ROWS_PER_PAGE
        pagination = None
        if dict_name:
            try:
                with database_engine.connect() as conn:
                    result_count = conn.execute(text(f'SELECT COUNT(*) FROM {dict_name}'))
                    for row in result_count:
                        count = int(row[0])
                    result = conn.execute(text(f'SELECT * FROM {dict_name} LIMIT {ROWS_PER_PAGE} OFFSET {start_at}'))
                    table_data = [tuple(row) for row in result]
                    table_desc = result.keys()
                    pagination = Pagination(page=page, total=count, search=False, record_name={dict_name},
                                            per_page=ROWS_PER_PAGE, css_framework='bootstrap4',
                                            prev_label='<', next_label='>', display_msg='')
            except Exception as err:
                flash(f'Ошибка: {str(err)}', 'danger')
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('dicts.html', master_mode=master_mode, table_desc=table_desc,
                               table_data=table_data, dict_name=dict_name, dict_form=dict_form,
                               pagination=pagination, login=login)
    except TemplateNotFound:
        return render_template(f'404.html')


@view_page.route('/compare')
@login_required
def compare_show():
    if master_mode:
        database_engine = database_mm_master_engine
    else:
        database_engine = database_mm_engine
    show_all = request.args.get('show_all', default='', type=str)
    show_diff = request.args.get('show_diff', default='', type=str)
    mm_dict_name = request.args.get('select_dict', default='', type=str)
    dict_form = DictForm(show_all=show_all, show_diff=show_diff, select_dict=mm_dict_name)
    pagination = None
    compare_data = []
    dict_name = ''
    try:
        try:
            mm_table_desc = []
            nsi_table_desc = []
            value_dict = {}
            update_dict = {}
            page = request.args.get(get_page_parameter(), type=int, default=1)
            nsi_dict_name = ''
            start_at = (page - 1) * ROWS_PER_PAGE
            limit_offset = f' LIMIT {ROWS_PER_PAGE} OFFSET {start_at}' if not show_all else ''
            pagination = None
            if mm_dict_name:
                with database_nsi_engine.connect() as conn_nsi:
                    result_table = conn_nsi.execute(select(nsi_tables_config.c.NSI_TABLE_NAME,
                                                           nsi_tables_config.c.COLUMN_MATCHING,
                                                           nsi_tables_config.c.COLUMN_UPDATE,
                                                           nsi_tables_config.c.DICT_NAME).where(
                                                                   nsi_tables_config.c.MMDB_TABLE_NAME == mm_dict_name))
                    for row in result_table:
                        row_tuple = tuple(row)
                        nsi_dict_name = row_tuple[0]
                        value_dict = loads(row_tuple[1])
                        update_dict = loads(row_tuple[2])
                        dict_name = row_tuple[3]
                    result_count = conn_nsi.execute(text(f'SELECT COUNT(*) FROM {nsi_dict_name}'))
                    for row in result_count:
                        count_nsi = int(row[0])
                    result = conn_nsi.execute(
                        text(f"""SELECT {",".join(["CAST(" + row + " AS UNSIGNED) as " + row for row in update_dict.values()])},
                                        {",".join(list(value_dict.values()))} 
                                 FROM {nsi_dict_name} 
                                 ORDER BY {",".join(["CAST(" + row + " AS UNSIGNED)" for row in update_dict.values()])} ASC{limit_offset}"""))
                    nsi_table_data = [list(row) for row in result]
                    nsi_table_desc = tuple(result.keys())
                with database_engine.connect() as conn_mm:
                    result_count = conn_mm.execute(text(f'SELECT COUNT(*) FROM {mm_dict_name}'))

                    for row in result_count:
                        count_mm = int(row[0])
                    result = conn_mm.execute(text(f"""SELECT {",".join(list(update_dict.keys()))},
                                                             {",".join(list(value_dict.keys()))} 
                                                      FROM {mm_dict_name} 
                                                      ORDER BY {",".join(list(update_dict.keys()))} ASC{limit_offset}"""))
                    mm_table_data = [list(row) for row in result]
                    mm_table_desc = tuple(result.keys())
                count = count_nsi if count_nsi > count_mm else count_mm
                table_data = list(zip_longest(mm_table_data, nsi_table_data))
                table_data = [list(row) for row in table_data]
                for index, row_table in enumerate(table_data):
                    if row_table[0] is None:
                        table_data[index][0] = list('')
                    elif row_table[1] is None:
                        table_data[index][1] = list('')
                diff_list = []
                for row in table_data:
                    if md5(','.join([str(cell) for cell in row[0]]).encode('utf-8')).hexdigest() == md5(','.join([str(cell) for cell in row[1]]).encode('utf-8')).hexdigest():
                        for index, cell in enumerate(row[0]):
                            row[0][index] = f'<td style="background-color: #e7f2dc">{cell}</td>'
                        for index, cell in enumerate(row[1]):
                            row[1][index] = f'<td style="background-color: #e7f2dc">{cell}</td>'
                    else:
                        for index, cell in enumerate(row[0]):
                            row[0][index] = f'<td style="background-color: #edcccc">{cell}</td>'
                        for index, cell in enumerate(row[1]):
                            row[1][index] = f'<td style="background-color: #edcccc">{cell}</td>'
                        diff_list.append(row)
                compare_data = [row[0] + row[1] for row in table_data] if not show_diff else [row[0] + row[1] for row in diff_list]
                if not show_all:
                    pagination = Pagination(page=page, total=count, search=False, per_page=ROWS_PER_PAGE,
                                            css_framework='bootstrap4', prev_label='<', next_label='>',
                                            display_msg='', dict_name=dict_name)
        except Exception as err:
           flash(f'Ошибка: {str(err)}', 'danger')
        login = ''
        if current_user.is_authenticated:
            login = current_user.name
        return render_template('compare.html', master_mode=master_mode, dict_form=dict_form, table_data=compare_data,
                               mm_table_desc=mm_table_desc, nsi_table_desc=nsi_table_desc, dict_name=dict_name,
                               pagination=pagination, login=login)
    except TemplateNotFound:
        return render_template(f'404.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        try:
            user = User.query.filter_by(login=login_form.login.data).first()
            if user and user.check_password(password=login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('view_page.operations_show'))
            flash('Неверное имя пользователя/пароль', 'danger')
            return redirect(url_for('auth.login'))
        except Exception as err:
           flash(f'Ошибка: {str(err)}', 'danger')
    return render_template('login.html', login_form=login_form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view_page.index_show'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash(f'Авторизуйтесь для доступа к странице', 'warning')
    return redirect(url_for('auth.login'))
