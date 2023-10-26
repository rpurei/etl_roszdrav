from ..tasks.tables import nsi_tables_config
from ..models.models import database_nsi_engine
from flask_wtf import FlaskForm
from flask import flash
from wtforms import SubmitField, widgets, SelectMultipleField, HiddenField, SelectField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Optional, DataRequired
from datetime import date
from sqlalchemy import select


class SearchForm(FlaskForm):
    dict_list = []
    try:
        with database_nsi_engine.connect() as conn:
            result = conn.execute(select(nsi_tables_config))
            for row in result:
                row_tuple = tuple(row)
                dict_list.append((row_tuple[3], row_tuple[4]))
    except Exception as err:
        flash(str(err), 'danger')
    dict_list.insert(0, ('All', 'Все справочники'))
    dt = DateField('DatePicker', format='%Y-%m-%d', default=date.today(), validators=[Optional()])
    select_dict = SelectField(u'Словарь', choices=dict_list, validators=[InputRequired()],
                              render_kw={'style': 'width: 250px'},)


class DictForm(FlaskForm):
    dict_list = []
    try:
        with database_nsi_engine.connect() as conn:
            result = conn.execute(select(nsi_tables_config))
            for row in result:
                row_tuple = tuple(row)
                dict_list.append((row_tuple[3], row_tuple[4]))
    except Exception as err:
        flash(str(err), 'danger')
    show_all = BooleanField('Все')
    show_diff = BooleanField('Только отличающиеся')
    select_dict = SelectField(u'Словарь', choices=dict_list, validators=[InputRequired()], render_kw={'style': 'width: 250px'}, )


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProcessDictionariesForm(FlaskForm):
    dict_list = []
    try:
        with database_nsi_engine.connect() as conn:
            result = conn.execute(select(nsi_tables_config))
            for row in result:
                row_tuple = tuple(row)
                dict_list.append((row_tuple[3], row_tuple[4]))
    except Exception as err:
        flash(str(err), 'danger')
    checkboxes_dict = MultiCheckboxField('Label', choices=dict_list)
    operation_dict = MultiCheckboxField('Label', choices=[('download', 'Загрузка справочников'),
                                                          ('update', 'Обновление справочников'),
                                                          ('differ', 'Только отличающиеся справочники'),
                                                          ('check', 'Сравнение справочников'),
                                                          ('rollback', 'Откат обновления справочников'),
                                                          ('notify', 'Отправка уведомления в чат Б24')
                                                          ])
    task_start = HiddenField()
    task_args = HiddenField()
    task_id = HiddenField()
    master_mode = HiddenField()
    submit = SubmitField('Запустить операцию')


class LoginForm(FlaskForm):
    login = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')


class ConfigEditForm(FlaskForm):
    ID = HiddenField()
    NSI_TABLE_NAME = StringField('Имя таблицы НСИ', validators=[DataRequired()])
    OID = StringField('OID справочника', validators=[DataRequired()])
    MMDB_TABLE_NAME = StringField('Имя таблицы MM', validators=[DataRequired()])
    DICT_NAME = StringField('Название справочника', validators=[DataRequired()])
    COLUMN_MATCHING = StringField('Соответствие полей', validators=[Optional()], render_kw={'placeholder': '{\'ПОЛЕ_ММ\': \'ПОЛЕ_НСИ\'}', 'style': 'width: 220px'})
    COLUMN_UPDATE = StringField('Ключ', validators=[Optional()], render_kw={'placeholder': '{\'ПОЛЕ_ММ\': \'ПОЛЕ_НСИ\'}', 'style': 'width: 220px'})
    COLUMN_CONVERT = StringField('Преобразование', validators=[Optional()], render_kw={'style': 'width: 100px'})
    COLUMN_EXTRA = StringField('Доп.параметры', validators=[Optional()], render_kw={'style': 'width: 100px'})


class ConfigDeleteForm(FlaskForm):
    ID = HiddenField()
    DICT_NAME = HiddenField()


class MasterAccessForm(FlaskForm):
    code = StringField('Код подтверждения')
    confirm = StringField('Введите код', validators=[DataRequired()])
