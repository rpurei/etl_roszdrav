from sqlalchemy import (Table, Column, Integer, String, MetaData, Enum, PickleType, DateTime, Text, BigInteger,
                        Date, ForeignKey)
import pickle
meta = MetaData()

nsi_tables_config = Table(
    'nsi_tables_config', meta,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('NSI_TABLE_NAME', String(256)),
    Column('OID', String(128)),
    Column('MMDB_TABLE_NAME', String(256)),
    Column('DICT_NAME', String(256)),
    Column('COLUMN_MATCHING', PickleType),
    Column('COLUMN_UPDATE', PickleType),
    Column('COLUMN_CONVERT', PickleType),
    Column('COLUMN_EXTRA', PickleType)
)


nsi_tables_status = Table(
    'nsi_tables_status', meta,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('SESSION_ID', String(32)),
    Column('OPER_START', DateTime),
    Column('OPER_END', DateTime),
    Column('OPER_TYPE', Enum('Download', 'Update', 'Rollback', 'Compare')),
    Column('OPER_STATUS', Enum('Success', 'Warning', 'Critical', 'Started')),
    Column('TABLE_ID', Integer, ForeignKey("nsi_tables_config.ID")),
    Column('OPER_DESC', Text)
)

b_hlbd_nsi_accreditation_standarts = Table(
    'b_hlbd_nsi_accreditation_standarts', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_STANDART', Text)
)

b_hlbd_nsi_accreditation_types = Table(
    'b_hlbd_nsi_accreditation_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_TYPE', Text)
)

b_hlbd_nsi_address_types = Table(
    'b_hlbd_nsi_address_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_ADDRESS_TYPE', Text)
)

b_hlbd_bacteries = Table(
    'b_hlbd_bacteries', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NSI_ID', Integer),
    Column('UF_ID_LEVEL', Integer),
    Column('UF_PARENT_ID', Integer),
    Column('UF_NAME', Text),
    Column('UF_NAME_FULL', Text),
    Column('UF_CHILDREN', Integer),
    Column('UF_SYN', Text),
    Column('UF_ID_SNOMED', BigInteger),
    Column('UF_SORT', Integer),
    Column('UF_GRAM_PROBE', Text)
)

b_hlbd_nsi_bad_habitat = Table(
    'b_hlbd_nsi_bad_habitat', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_SYN', Text),
    Column('UF_ID_SNOMED', Text),
    Column('UF_IS_ACTIVE', Integer)
)

b_hlbd_blood_groups_dictionary = Table(
    'b_hlbd_blood_groups_dictionary', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Integer),
    Column('UF_NAME', Text),
    Column('UF_SHORT_NAME', Text),
    Column('UF_SIGN_RES_RESULT', Integer),
    Column('UF_SIGN_RES_ALL', Integer),
    Column('UF_SIGN_RES_FOR_SPEC', Integer),
    Column('UF_SORT', Integer),
    Column('UF_ACTIVE', Integer)
)

b_hlbd_nsi_citizen_agents = Table(
    'b_hlbd_nsi_citizen_agents', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_AGENT_CODE', Integer),
    Column('UF_AGENT_NAME', Text)
)

b_hlbd_dictionary_departments_cabinets = Table(
    'b_hlbd_dictionary_departments_cabinets', meta,
    Column('UF_OID_ORGANIZATION', Text),
    Column('UF_OID_DEPARTMENT', Text),
    Column('UF_DEPARTMENT_TYPE_I', Integer),
    Column('UF_DEPARTMENT_TYPE', Text),
    Column('UF_DEPARTMENT_CLASS_', Integer),
    Column('UF_DEPARTMENT_CLASS', Text),
    Column('UF_DEPARTMENT_IS_STA', Text),
    Column('UF_DEPARTMENT_STANDA', Text),
    Column('UF_OID_DESK', Text),
    Column('UF_DESK_NAME', Text),
    Column('UF_DESK_TYPE', Text),
    Column('UF_DESK_TYPE_NAME', Text),
    Column('UF_CABINET_TYPE_ID', Integer),
    Column('UF_CABINET_NAME', Text),
    Column('UF_CABINET_COUNT', Text),
    Column('UF_CABINET_P_TYPE', Integer),
    Column('UF_CABINET_P_NAME', Text),
    Column('UF_CABINET_P_COUNT', Integer),
    Column('UF_CABINET_R_D_COUNT', Integer),
    Column('UF_BUILDING_ID', Integer),
    Column('UF_BUILDING_NAME', Text),
    Column('UF_BUILDING_C_YEAR', Integer),
    Column('UF_BUILDING_F_COUNT', Integer),
    Column('UF_BUILDING_BROKEN', Text),
    Column('UF_POSTAL_CODE', Text),
    Column('UF_CADASTRE_ID', Text),
    Column('UF_LATITUDE', Text),
    Column('UF_LONGTITUDE', Text),
    Column('UF_REGION_CODE_ID', Integer),
    Column('UF_REGION_NAME', Text),
    Column('UF_REGION_ID', Text),
    Column('UF_STREET_ID', Text),
    Column('UF_HOUSE_ID', Text),
    Column('UF_TOWN_PREFIX', Text),
    Column('UF_TOWN_NAME', Text),
    Column('UF_STREET_PREFIX', Text),
    Column('UF_STREET_NAME', Text),
    Column('UF_HOUSE_NUMBER', Text),
    Column('UF_HOUSE_B_NUMBER', Text),
    Column('UF_HOUSE_U_NUMBER', Text),
    Column('UF_FIAS_VERSION_ID', Integer),
    Column('UF_DEPARTMENT_NAME', Text),
    Column('UF_CREATE_DATE', DateTime),
    Column('UF_MODIFY_DATE', DateTime),
    Column('UF_REMOVE_DATE', DateTime),
    Column('UF_DESK_REMOVE_DATE', DateTime),
    Column('UF_BUILDING_C_DATE', DateTime),
    Column('UF_BUILDING_M_DATE', DateTime),
    Column('UF_METRO', Text),
    Column('UF_JOB_GRAPPH', Text),
    Column('UF_PHONE', Text),
    Column('UF_WEBSITE', Text),
    Column('UF_EMAIL', Text),
    Column('UF_NSI_UNITS_ID', Integer),
    Column('UF_OID_DESK_MD5', String(32)),
    Column('UF_MD5', String(32))
)

b_hlbd_nsi_category_medic_workers = Table(
    'b_hlbd_nsi_category_medic_workers', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_S_NAME', Text)
)

b_hlbd_consult_types = Table(
    'b_hlbd_consult_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_nsi_countries = Table(
    'b_hlbd_nsi_countries', meta,
    #Column('ID', Integer, primary_key=True),
    Column('UF_CODE', Text),
    Column('UF_NAME', Text),
    Column('UF_A1', Text),
    Column('UF_A2', Text)
)

b_hlbd_nsi_credentials = Table(
    'b_hlbd_nsi_credentials', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_DOC_NAME', Text),
    Column('UF_ACTIVE', Integer),
    Column('UF_SHORT_NAME', Text)
)

b_hlbd_nsi_cure_application_types = Table(
    'b_hlbd_nsi_cure_application_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_APP_WAY_RU', Text),
    Column('UF_APP_WAY_ENG', Text),
    Column('UF_PARENT_ID', Integer),
    Column('UF_SORT', Integer, default=100)
)

b_hlbd_decret_groups = Table(
    'b_hlbd_decret_groups', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_diplomas = Table(
    'b_hlbd_diplomas', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_ID_PROFESSION', Integer),
    Column('UF_END_DATE', Date),
    Column('UF_IS_ACTIVE', Integer)
)

b_hlbd_diagnoses = Table(
    'b_hlbd_diagnoses', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_REC_CODE', Text),
    Column('UF_MKB_CODE', Text),
    Column('UF_MKB_NAME', Text),
    Column('UF_ID_PARENT', Integer),
    Column('UF_ADDL_CODE', Text),
    Column('UF_ACTUAL', Integer),
    Column('UF_DATE', Date),
    Column('UF_MKB_NAME_ENG', Text),
    Column('UF_AG_CLASS', Integer)
)

b_hlbd_doc_cda_fields = Table(
    'b_hlbd_doc_cda_fields', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_blood_donate_dictionary = Table(
    'b_hlbd_blood_donate_dictionary', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_SORT', Integer),
    Column('UF_ACTIVE', Integer, default=1)
)

b_hlbd_family_types = Table(
    'b_hlbd_family_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_firing_reasons = Table(
    'b_hlbd_firing_reasons', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_REASON', Text)
)

b_hlbd_insurance_companies = Table(
    'b_hlbd_insurance_companies', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_ERM_INSURANC_NAME', Text),
    Column('UF_SMOCOD', Text),
    Column('UF_OGRN', Text),
    Column('UF_KPP', Text),
    Column('UF_NAM_SMOP', Text),
    Column('UF_NAM_SMOK', Text),
    Column('UF_ADDR_F', Text),
    Column('UF_FAM_RUK', Text),
    Column('UF_IM_RUK', Text),
    Column('UF_OT_RUK', Text),
    Column('UF_PHONE', Text),
    Column('UF_FAX', Text),
    Column('UF_HOT_LINE', Text),
    Column('UF_E_MAIL', Text),
    Column('UF_N_DOC', Text),
    Column('UF_D_START', Date),
    Column('UF_DATE_E', Date),
    Column('UF_D_BEGIN', Date),
    Column('UF_D_END', Date),
    Column('UF_SORT', Integer, default=100),
    Column('UF_ACTIVE', Integer, default=1)
)

b_hlbd_health_damage = Table(
    'b_hlbd_health_damage', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_SYN', Text),
    Column('UF_ID_SNOMED', Text),
    Column('UF_SORT', Integer)
)

b_hlbd_nsi_postgraduate_education_types = Table(
    'b_hlbd_nsi_postgraduate_education_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_TYPE', Text)
)

b_hlbd_dictionary_laboratory_and_samples = Table(
    'b_hlbd_dictionary_laboratory_and_samples', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NSI_ID', Integer),
    Column('UF_MATTER_GROUP', Text),
    Column('UF_MATTER', Text),
    Column('UF_SPECIMEN', Text),
    Column('UF_SORT', Integer),
    Column('UF_ACTIVE', Integer, default=1)
)

b_hlbd_nsi_lab_tests_dictionary = Table(
    'b_hlbd_nsi_lab_tests_dictionary', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_LOINC', Text),
    Column('UF_FULL_NAME', Text),
    Column('UF_ENGLISH_NAME', Text),
    Column('UF_SHORT_NAME', Text),
    Column('UF_SYNONYMS', Text),
    Column('UF_ANALYTE', Text),
    Column('UF_SPEC_ANALYTE', Text),
    Column('UF_MEASUREMENT', Text),
    Column('UF_UNIT', Text),
    Column('UF_SPECIMEN', Text),
    Column('UF_TIMECHAR', Text)
)

b_hlbd_marital_status = Table(
    'b_hlbd_marital_status', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_DESCR', Text)
)

b_hlbd_nsi_med_knowledge = Table(
    'b_hlbd_nsi_med_knowledge', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_QUALITY', Text),
    Column('UF_SORT', Text)
)

b_hlbd_nsi_medical_care_types = Table(
    'b_hlbd_nsi_medical_care_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NSI_ID', Integer),
    Column('UF_PARENT', Integer),
    Column('UF_NAME', Text),
    Column('UF_SORT', Integer),
    Column('UF_ACTIVE', Integer)
)

b_hlbd_medical_context_types = Table(
    'b_hlbd_medical_context_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_nsi_medical_functions = Table(
    'b_hlbd_nsi_medical_functions', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Text),
    Column('UF_STR_NUM', Text),
    Column('UF_ROLE_NAME', Text),
    Column('UF_GROUP_BIT', Text),
    Column('UF_SERTIFICATE_BIT', Text),
    Column('UF_FORM_CODE', Text),
    Column('UF_ACTUAL_BIT', Integer),
    Column('UF_END_DATE', Date),
    Column('UF_COMMENTS', Text)
)

b_hlbd_nsi_medical_roles = Table(
    'b_hlbd_nsi_medical_roles', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_PARENT_ID', Text),
    Column('UF_ACTUAL_BIT', Integer),
    Column('UF_END_DATE', Date),
    Column('UF_SNOMED', Text)
)

b_hlbd_nsi_medics_quality = Table(
    'b_hlbd_nsi_medics_quality', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_MEDIC_QUALITY', Text),
    Column('UF_END_DATE', Date)
)

b_hlbd_mushrooms = Table(
    'b_hlbd_mushrooms', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NSI_ID', Integer),
    Column('UF_ID_LEVEL', Integer),
    Column('UF_PARENT_ID', Integer),
    Column('UF_NAME', Text),
    Column('UF_NAME_FULL', Text),
    Column('UF_CHILDREN', Integer),
    Column('UF_SYN', Text),
    Column('UF_ID_SNOMED', Integer),
    Column('UF_SORT', Integer)
)

b_hlbd_nsi_nationality = Table(
    'b_hlbd_nsi_nationality', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_S_NAME', Text)
)

b_hlbd_nsi_nmu = Table(
    'b_hlbd_nsi_nmu', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_S_CODE', Text),
    Column('UF_NAME', Text),
    Column('UF_REL', Integer),
    Column('UF_DATEOUT', Date)
)

b_hlbd_patologic_reaction_types = Table(
    'b_hlbd_patologic_reaction_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_PARENT_ID', Integer),
    Column('UF_ID_SNOMED', Text)
)

b_hlbd_patologic_reactions = Table(
    'b_hlbd_patologic_reactions', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_ID_SNOMED', Integer),
    Column('UF_SYN', Text)
)

b_hlbd_nsi_units = Table(
    'b_hlbd_nsi_units', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_OID', Text),
    Column('UF_OLD_OID', Text),
    Column('UF_NAME_FULL', Text),
    Column('UF_NAME_SHORT', Text),
    Column('UF_PARENT_ID', Integer),
    Column('UF_MED_SUBJECT_ID', Integer),
    Column('UF_MED_SUBJECT_NAME', Text),
    Column('UF_INN', Text),
    Column('UF_KPP', Text),
    Column('UF_OGRN', Text),
    Column('UF_REGION_ID', Integer),
    Column('UF_REGION_NAME', Text),
    Column('UF_ORG_TYPE', Integer),
    Column('UF_MO_DEPT_NAME', Text),
    Column('UF_FOUNDER', Text),
    Column('UF_DEL_DATE', Date),
    Column('UF_DEL_REASON', Text),
    Column('UF_CREATE_DATE', Date),
    Column('UF_MODIFY_DATE', Date),
    Column('UF_MO_LEVEL', Text),
    Column('UF_MO_AGENCY_KIND', Text),
    Column('UF_PROF_AGENCY_KIND', Text),
    Column('UF_POST_INDEX', Text),
    Column('UF_CAD_NUMBER', Text),
    Column('UF_LAT', Text),
    Column('UF_LONG', Text),
    Column('UF_FIAS_VERSION', Text),
    Column('UF_AOID_AREA', Text),
    Column('UF_AOID_STREET', Text),
    Column('UF_HOUSE_ID', Text),
    Column('UF_ADDR_REGION_ID', Text),
    Column('UF_ADDR_REGION_NAME', Text),
    Column('UF_TERRITORY_CODE', Text),
    Column('UF_IS_FEDERAL_CITY', Text),
    Column('UF_AREA_NAME', Text),
    Column('UF_PREFIX_AREA', Text),
    Column('UF_STREET_NAME', Text),
    Column('UF_PREFIX_STREET', Text),
    Column('UF_HOUSE', Text),
    Column('UF_BUILDING', Text),
    Column('UF_STRUCT', Text),
    Column('UF_MAIN_PHONE', Text),
    Column('UF_REG_PHONE', Text),
    Column('UF_OKPO', Text),
    Column('UF_LOGO', Text),
    Column('UF_METRO', Text),
    Column('UF_JOB_GRAPPH', Text),
    Column('UF_MO_PHONE', Text),
    Column('UF_WEBSITE', Text),
    Column('UF_NAME_FULL_ENG', Text),
    Column('UF_NAME_SHORT_ENG', Text),
    Column('UF_ADDRESS_FULL_ENG', Text),
    Column('UF_TITLE', Text),
    Column('UF_EMAIL', Text),
    Column('UF_PHOTO', Text),
    Column('UF_CREATE_RESEARCH', Integer),
    Column('UF_SOURCE', Integer, default=1),
    Column('UF_USER_CREATE', Integer)
)

b_hlbd_prof_study_status = Table(
    'b_hlbd_prof_study_status', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Integer),
    Column('UF_NAME', Text),
    Column('UF_ORDER_ID', Text),
    Column('UF_STUDY_ID', Text),
    Column('UF_MEDICAL_EMP', Text),
    Column('UF_ACTUAL_BIT', Text),
    Column('UF_END_DATE', Date)
)

b_hlbd_nsi_relation_types = Table(
    'b_hlbd_nsi_relation_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_RELATION_NAME', Text)
)

b_hlbd_nsi_rf_subjects = Table(
    'b_hlbd_nsi_rf_subjects', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_ID_AREA', Integer),
    Column('UF_AREA_NAME', Text),
    Column('UF_PARENT_ID', Integer),
    Column('UF_DATE_START', Date),
    Column('UF_DATE_STOP', Date),
    Column('UF_SORT_ORDER', Integer),
    Column('UF_OIV', Text),
    Column('UF_OKATO', Text)
)

b_hlbd_nsi_study_owner = Table(
    'b_hlbd_nsi_study_owner', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Text),
    Column('UF_OWNER_NAME', Text),
    Column('UF_OWNER_ID', Text),
    Column('UF_LOCATION', Text)
)

b_hlbd_surgery_types = Table(
    'b_hlbd_surgery_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Integer),
    Column('UF_NAME', Text),
    Column('UF_ID_FORM14', Text)
)

b_hlbd_tuberculosis_housing = Table(
    'b_hlbd_tuberculosis_housing', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text)
)

b_hlbd_vital_parameters = Table(
    'b_hlbd_vital_parameters', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NAME', Text),
    Column('UF_UNITS', Text)
)

b_hlbd_nsi_work_termination_reasons = Table(
    'b_hlbd_nsi_work_termination_reasons', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_PARENT_ID', Integer),
    Column('UF_REASON', Text)
)

b_hlbd_working_stress = Table(
    'b_hlbd_working_stress', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_ID_FACTOR_GROUP', Integer),
    Column('UF_NAME', Text),
    Column('UF_PARENT_ID', Integer),
    Column('UF_ID_SNOMED', Text),
    Column('UF_IS_ACTIVE', Integer)
)

b_hlbd_nsi_medical_equipment_types = Table(
    'b_hlbd_nsi_medical_equipment_types', meta,
    Column('ID', Integer, primary_key=True),
    Column('UF_NSI_ID', Integer),
    Column('UF_PARENT', Integer),
    Column('UF_NAME', Text),
    Column('UF_REL', Integer),
    Column('UF_DATEOUT', Date),
    Column('UF_SORT', Integer),
    Column('UF_ACTIVE', Integer)
)

b_hlbd_nsi_medical_schools_extended = Table(
    'b_hlbd_nsi_medical_schools_extended', meta,
    Column('ID', Integer, primary_key=True),
    Column('NAME_FULL', Text),
    Column('NAME_SHORT', Text),
    Column('NAME_BEGIN_DATE', Date),
    Column('NAME_END_DATE', Date),
    Column('SCHOOL_OID', Text),
    Column('REGION_ID', Integer)
)


initial_data = [{'NSI_TABLE_NAME': 'nsi_accreditation_standarts',                           # 1
                 'OID': '1.2.643.5.1.13.13.99.2.283',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_accreditation_standarts',
                 'DICT_NAME': 'Стандарт аккредитации',
                 'COLUMN_MATCHING': pickle.dumps({'UF_STANDART': 'profStandard'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_accreditation_types',                               # 2
                 'OID': '1.2.643.5.1.13.13.99.2.295',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_accreditation_types',
                 'DICT_NAME': 'Вид аккредитации',
                 'COLUMN_MATCHING': pickle.dumps({'UF_TYPE': 'accreditationKind'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_address_types',                                     # 3
                 'OID': '1.2.643.5.1.13.13.99.2.53',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_address_types',
                 'DICT_NAME': 'ФР7Н. Справочник типов адреса пациента',
                 'COLUMN_MATCHING': pickle.dumps({'UF_ADDRESS_TYPE': 'ADDRESS_TYPE'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_bacteries',                                         # 4
                 'OID': '1.2.643.5.1.13.13.11.1087',
                 'MMDB_TABLE_NAME': 'b_hlbd_bacteries',
                 'DICT_NAME': 'Федеральный справочник лабораторных исследований. Справочник бактерий',
                 'COLUMN_MATCHING': pickle.dumps({'UF_ID_LEVEL': 'LEVEL',
                                                    'UF_PARENT_ID': 'ID_PARENT',
                                                    'UF_NAME': 'FORMATNAME',
                                                    'UF_NAME_FULL': 'FULLNAME',
                                                    'UF_CHILDREN': 'CHILDCOUNT',
                                                    'UF_SYN': 'SYNONIMS',
                                                    'UF_ID_SNOMED': 'SNOMED',
                                                    'UF_SORT': 'SORT',
                                                    'UF_GRAM_PROBE': 'GRAM'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_bad_habitat',                                       # 5
                 'OID': '1.2.643.5.1.13.13.11.1058',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_bad_habitat',
                 'DICT_NAME': 'Вредные привычки',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_SYN': 'SYNONYM',
                                                    'UF_ID_SNOMED': 'SCTID',
                                                    'UF_IS_ACTIVE': 'REL'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_blood_groups',                                      # 6
                 'OID': '1.2.643.5.1.13.13.11.1061',
                 'MMDB_TABLE_NAME': 'b_hlbd_blood_groups_dictionary',
                 'DICT_NAME': 'Классификатор донорской крови, компонентов и препаратов крови',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PARENT',
                                                    'UF_NAME': 'NAME_FULL',
                                                    'UF_SHORT_NAME': 'NAME_SHOT',
                                                    'UF_SIGN_RES_RESULT': 'SING1',
                                                    'UF_SIGN_RES_ALL': 'SING2',
                                                    'UF_SIGN_RES_FOR_SPEC': 'SING3'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_citizen_agents',                                    # 7
                 'OID': '1.2.643.5.1.13.13.99.2.444',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_citizen_agents',
                 'DICT_NAME': 'Классификатор представителей гражданина',
                 'COLUMN_MATCHING': pickle.dumps({'UF_AGENT_CODE': 'CODE',
                                                    'UF_AGENT_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_departments_cabinets',                              # 8
                 'OID': '1.2.643.5.1.13.13.99.2.115',
                 'MMDB_TABLE_NAME': 'b_hlbd_dictionary_departments_cabinets',
                 'DICT_NAME': 'Справочник отделений МО',
                 'COLUMN_MATCHING': pickle.dumps({'UF_OID_ORGANIZATION': 'mo_oid',
                                                  'UF_OID_DEPARTMENT': 'depart_oid',
                                                  'UF_DEPARTMENT_TYPE_I': 'depart_type_id',
                                                  'UF_DEPARTMENT_TYPE': 'depart_type_name',
                                                  'UF_DEPARTMENT_CLASS_': 'depart_kind_id',
                                                  'UF_DEPARTMENT_CLASS': 'depart_kind_name',
                                                  'UF_DEPARTMENT_IS_STA': 'separate_depart_boolean',
                                                  'UF_DEPARTMENT_STANDA': 'separate_depart_text',
                                                  'UF_OID_DESK': 'oid',
                                                  'UF_DESK_NAME': 'hospital_name',
                                                  'UF_DESK_TYPE': 'hospital_subdivision_id',
                                                  'UF_DESK_TYPE_NAME': 'hospital_subdivision_name',
                                                  'UF_CABINET_TYPE_ID': 'ambulance_subdivision_id',
                                                  'UF_CABINET_NAME': 'ambulance_subdivision_name',
                                                  'UF_CABINET_COUNT': 'ambulance_room_count',
                                                  'UF_CABINET_P_TYPE': 'lab_subdivision_id',
                                                  'UF_CABINET_P_NAME': 'lab_subdivision_name',
                                                  'UF_CABINET_P_COUNT': 'lab_room_count',
                                                  'UF_CABINET_R_D_COUNT': 'lab_exam_per_shift',
                                                  'UF_BUILDING_ID': 'building_id',
                                                  'UF_BUILDING_NAME': 'building_name',
                                                  'UF_BUILDING_C_YEAR': 'building_build_year',
                                                  'UF_BUILDING_F_COUNT': 'building_floor_count',
                                                  'UF_BUILDING_BROKEN': 'building_has_trouble',
                                                  'UF_POSTAL_CODE': 'building_address_post_index',
                                                  'UF_CADASTRE_ID': 'building_address_cadastral_number',
                                                  'UF_LATITUDE': 'building_address_latitude',
                                                  'UF_LONGTITUDE': 'building_address_longtitude',
                                                  'UF_REGION_CODE_ID': 'building_address_region_id',
                                                  'UF_REGION_NAME': 'building_address_region_name',
                                                  'UF_REGION_ID': 'building_address_aoid_area',
                                                  'UF_STREET_ID': 'building_address_aoid_street',
                                                  'UF_HOUSE_ID': 'building_address_houseid',
                                                  'UF_TOWN_PREFIX': 'building_address_prefix_area',
                                                  'UF_TOWN_NAME': 'building_address_area_name',
                                                  'UF_STREET_PREFIX': 'building_address_prefix_street',
                                                  'UF_STREET_NAME': 'building_address_street_name',
                                                  'UF_HOUSE_NUMBER': 'building_address_house',
                                                  'UF_HOUSE_B_NUMBER': 'building_address_building',
                                                  'UF_HOUSE_U_NUMBER': 'building_address_struct',
                                                  'UF_FIAS_VERSION_ID': 'building_address_fias_version',
                                                  'UF_DEPARTMENT_NAME': 'depart_name',
                                                  'UF_CREATE_DATE': 'depart_create_date',
                                                  'UF_MODIFY_DATE': 'depart_modify_date',
                                                  'UF_REMOVE_DATE': 'depart_liquidation_date',
                                                  'UF_DESK_REMOVE_DATE': 'hospital_liquidation_date',
                                                  'UF_BUILDING_C_DATE': 'building_create_date',
                                                  'UF_BUILDING_M_DATE': 'building_modify_date',
                                                  #'UF_OID_DESK_MD5': 'UF_OID_DESK_MD5',
                                                  'UF_MD5': 'UF_MD5'
                                                  }),
                 #'COLUMN_UPDATE': pickle.dumps({'UF_OID_DESK': 'oid'})},
                 'COLUMN_UPDATE': pickle.dumps({'UF_OID_DESK_MD5': 'UF_OID_DESK_MD5'})},
                {'NSI_TABLE_NAME': 'nsi_category_medic_workers',                            # 9
                 'OID': '1.2.643.5.1.13.13.11.1494',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_category_medic_workers',
                 'DICT_NAME': 'Квалификационные категории медицинских и фармацевтических работников',
                 'COLUMN_MATCHING': pickle.dumps({'UF_S_NAME': 'S_NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_consult_types',                                     # 10
                 'OID': '1.2.643.5.1.13.13.99.2.797',
                 'MMDB_TABLE_NAME': 'b_hlbd_consult_types',
                 'DICT_NAME': 'Справочник типов консультаций',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_countries',                                         # 11
                 'OID': '1.2.643.5.1.13.13.99.2.545',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_countries',
                 'DICT_NAME': 'Общероссийский классификатор стран мира',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME_SHORT',
                                                   'UF_A1': 'A2',
                                                   'UF_A2': 'A3'}),
                 'COLUMN_UPDATE': pickle.dumps({'UF_CODE': 'ID_NUMBER'})},
                {'NSI_TABLE_NAME': 'nsi_credentials',                                       # 12
                 'OID': '1.2.643.5.1.13.13.99.2.48',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_credentials',
                 'DICT_NAME': 'Документы, удостоверяющие личность',
                 'COLUMN_MATCHING': pickle.dumps({'UF_DOC_NAME': 'NAME',
                                                    'UF_ACTIVE': 'ACTUAL'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_cure_application_types',                            # 13
                 'OID': '1.2.643.5.1.13.13.11.1468',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_cure_application_types',
                 'DICT_NAME': 'Пути введения ЛС',
                 'COLUMN_MATCHING': pickle.dumps({'UF_APP_WAY_RU': 'NAME_RUS',
                                                    'UF_APP_WAY_ENG': 'NAME_ENG',
                                                    'UF_PARENT_ID': 'PARENT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_decret_groups',                                     # 14
                 'OID': '1.2.643.5.1.13.13.99.2.248',
                 'MMDB_TABLE_NAME': 'b_hlbd_decret_groups',
                 'DICT_NAME': 'ФНР. Классификатор принадлежности к декретированным группам',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'decreedGroup'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_diplomas',                                          # 15
                 'OID': '1.2.643.5.1.13.13.11.1075',
                 'MMDB_TABLE_NAME': 'b_hlbd_diplomas',
                 'DICT_NAME': 'Квалификации по диплому специалистов высшего и среднего профессионального образования',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_ID_PROFESSION': 'ID_SPECIALITY',
                                                    'UF_END_DATE': 'DATEOUT',
                                                    'UF_IS_ACTIVE': 'REL'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_disease',                                           # 16
                 'OID': '1.2.643.5.1.13.13.11.1005',
                 'MMDB_TABLE_NAME': 'b_hlbd_diagnoses',
                 'DICT_NAME': 'Диагнозы',
                 'COLUMN_MATCHING': pickle.dumps({'UF_REC_CODE': 'REC_CODE',
                                                    'UF_MKB_CODE': 'MKB_CODE',
                                                    'UF_MKB_NAME': 'MKB_NAME',
                                                    'UF_ID_PARENT': 'ID_PARENT',
                                                    'UF_ADDL_CODE': 'ADDL_CODE',
                                                    'UF_ACTUAL': 'ACTUAL',
                                                    'UF_DATE': 'DATE'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_doc_cda_fields',                                    # 17
                 'OID': '1.2.643.5.1.13.13.99.2.166',
                 'MMDB_TABLE_NAME': 'b_hlbd_doc_cda_fields',
                 'DICT_NAME': 'Кодируемые поля CDA документов',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_donated_blood',                                     # 18
                 'OID': '1.2.643.5.1.13.13.11.1386',
                 'MMDB_TABLE_NAME': 'b_hlbd_blood_donate_dictionary',
                 'DICT_NAME': 'Классификатор донорской крови, компонентов и препаратов крови',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_SORT': 'SORT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_family_types',                                      # 19
                 'OID': '1.2.643.5.1.13.13.99.2.435',
                 'MMDB_TABLE_NAME': 'b_hlbd_family_types',
                 'DICT_NAME': 'Классификатор социально-демографических типов семьи',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'CODE'})},
                {'NSI_TABLE_NAME': 'nsi_firing_reasons',                                    # 20
                 'OID': '1.2.643.5.1.13.2.1.1.217',
                 'MMDB_TABLE_NAME': 'b_hlbd_firing_reasons',
                 'DICT_NAME': 'Причина увольнения',
                 'COLUMN_MATCHING': pickle.dumps({'UF_REASON': 'S_NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_insurance_companies',                               # 21
                 'OID': '1.2.643.5.1.13.13.99.2.183',
                 'MMDB_TABLE_NAME': 'b_hlbd_insurance_companies',
                 'DICT_NAME': 'Страховые компании по полисам ОМС и ДМС',
                 'COLUMN_MATCHING': pickle.dumps({'UF_OGRN': 'OGRN',
                                                    'UF_KPP': 'KPP',
                                                    'UF_NAM_SMOP': 'NAM_SMOP',
                                                    'UF_NAM_SMOK': 'NAM_SMOK',
                                                    'UF_ADDR_F': 'ADDR_F',
                                                    'UF_FAM_RUK': 'FAM_RUK',
                                                    'UF_IM_RUK': 'IM_RUK',
                                                    'UF_OT_RUK': 'OT_RUK',
                                                    'UF_PHONE': 'PHONE',
                                                    'UF_FAX': 'FAX',
                                                    'UF_HOT_LINE': 'HOT_LINE',
                                                    'UF_E_MAIL': 'E_MAIL',
                                                    'UF_N_DOC': 'N_DOC',
                                                    'UF_D_START': 'D_START',
                                                    'UF_DATE_E': 'DATE_E',
                                                    'UF_D_BEGIN': 'D_BEGIN',
                                                    'UF_D_END': 'D_END'}),
                 'COLUMN_UPDATE': pickle.dumps({'UF_SMOCOD': 'SMOCOD'})},
                {'NSI_TABLE_NAME': 'nsi_health_damage',                                     # 22
                 'OID': '1.2.643.5.1.13.13.11.1006',
                 'MMDB_TABLE_NAME': 'b_hlbd_health_damage',
                 'DICT_NAME': 'Степень тяжести состояния пациента',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_SYN': 'SYN',
                                                    'UF_ID_SNOMED': 'SCTID',
                                                    'UF_SORT': 'SORT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_high_edu_programs',                                 # 23
                 'OID': '1.2.643.5.1.13.13.99.2.104',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_postgraduate_education_types',
                 'DICT_NAME': 'Программы послевузовского профессионального образования',
                 'COLUMN_MATCHING': pickle.dumps({'UF_TYPE': 'TYPE_NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_laboratory_materials_and_samples',                  # 24
                 'OID': '1.2.643.5.1.13.13.11.1081',
                 'MMDB_TABLE_NAME': 'b_hlbd_dictionary_laboratory_and_samples',
                 'DICT_NAME': 'Справочник лабораторных материалов и образцов',
                 'COLUMN_MATCHING': pickle.dumps({'UF_MATTER_GROUP': 'GROUP',
                                                  'UF_MATTER': 'MATTER',
                                                  'UF_SPECIMEN': 'SPECIMEN',
                                                  'UF_SORT': 'Sort'}),
                 'COLUMN_UPDATE': pickle.dumps({'UF_NSI_ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_laboratory_tests',                                  # 25
                 'OID': '1.2.643.5.1.13.13.11.1080',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_lab_tests_dictionary',
                 'DICT_NAME': 'Справочник лабораторных исследований',
                 'COLUMN_MATCHING': pickle.dumps({'UF_LOINC': 'LOINC',
                                                    'UF_FULL_NAME': 'FULLNAME',
                                                    'UF_ENGLISH_NAME': 'ENGLISHNAME',
                                                    'UF_SHORT_NAME': 'SHORTNAME',
                                                    'UF_SYNONYMS': 'SYNONYMS',
                                                    'UF_ANALYTE': 'ANALYTE',
                                                    'UF_SPEC_ANALYTE': 'SPECANALYTE',
                                                    'UF_MEASUREMENT': 'MEASUREMENT',
                                                    'UF_UNIT': 'UNIT',
                                                    'UF_SPECIMEN': 'SPECIMEN',
                                                    'UF_TIMECHAR': 'TIMECHAR'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_marital_status',                                    # 26
                 'OID': '1.2.643.5.1.13.13.99.2.15',
                 'MMDB_TABLE_NAME': 'b_hlbd_marital_status',
                 'DICT_NAME': 'Семейное положение',
                 'COLUMN_MATCHING': pickle.dumps({'UF_DESCR': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_med_knowledge',                                     # 27
                 'OID': '1.2.643.5.1.13.13.99.2.193',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_med_knowledge',
                 'DICT_NAME': 'Тип образования мед.работников',
                 'COLUMN_MATCHING': pickle.dumps({'UF_QUALITY': 'educationType'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_medical_care_types',                                # 28
                 'OID': '1.2.643.5.1.13.13.11.1034',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medical_care_types',
                 'DICT_NAME': 'Виды медицинской помощи',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT': 'PARENT',
                                                    'UF_NAME': 'NAME',
                                                    'UF_SORT': 'SORT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medical_context_types',                             # 29
                 'OID': '1.2.643.5.1.13.13.11.1009',
                 'MMDB_TABLE_NAME': 'b_hlbd_medical_context_types',
                 'DICT_NAME': 'Справочник видов медицинских направлений',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medical_functions',                                 # 30
                 'OID': '1.2.643.5.1.13.13.11.1002',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medical_functions',
                 'DICT_NAME': 'Тип должности',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PID',
                                                    'UF_ROLE_NAME': 'NAME',
                                                    'UF_GROUP_BIT': 'GROUP',
                                                    'UF_FORM_CODE': 'FORM_30',
                                                    'UF_ACTUAL_BIT': 'ACTUAL',
                                                    'UF_END_DATE': 'DATA_END',
                                                    'UF_COMMENTS': 'COMMENT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medical_roles',                                     # 31
                 'OID': '1.2.643.5.1.13.13.11.1066',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medical_roles',
                 'DICT_NAME': 'Номенклатура специальностей',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_PARENT_ID': 'PARENT',
                                                    'UF_ACTUAL_BIT': 'REL',
                                                    'UF_END_DATE': 'DATEOUT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medics_quality',                                    # 32
                 'OID': '1.2.643.5.1.13.13.99.2.171',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medics_quality',
                 'DICT_NAME': 'Квалификация мед.персонала',
                 'COLUMN_MATCHING': pickle.dumps({'UF_MEDIC_QUALITY': 'qualification',
                                                    'UF_END_DATE': 'date_end'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_mushrooms',                                         # 33
                 'OID': '1.2.643.5.1.13.13.11.1088',
                 'MMDB_TABLE_NAME': 'b_hlbd_mushrooms',
                 'DICT_NAME': 'Федеральный справочник лабораторных исследований. Справочник грибов',
                 'COLUMN_MATCHING': pickle.dumps({'UF_ID_LEVEL': 'LEVEL',
                                                    'UF_PARENT_ID': 'ID_PARENT',
                                                    'UF_NAME': 'FORMATNAME',
                                                    'UF_NAME_FULL': 'FULLNAME',
                                                    'UF_CHILDREN': 'CHILDCOUNT',
                                                    'UF_SYN': 'SYNONIMS',
                                                    'UF_ID_SNOMED': 'SNOMED',
                                                    'UF_SORT': 'SORT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_nationality',                                       # 34
                 'OID': '1.2.643.5.1.13.13.99.2.315',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_nationality',
                 'DICT_NAME': 'Классификатор Гражданства',
                 'COLUMN_MATCHING': pickle.dumps({'UF_S_NAME': 'S_NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_nmu',                                               # 35
                 'OID': '1.2.643.5.1.13.13.11.1070',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_nmu',
                 'DICT_NAME': 'Медицинские услуги',
                 'COLUMN_MATCHING': pickle.dumps({'UF_S_CODE': 'S_CODE',
                                                    'UF_NAME': 'NAME',
                                                    'UF_REL': 'REL',
                                                    'UF_DATEOUT': 'DATEOUT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_patologic_reaction_types',                          # 36
                 'OID': '1.2.643.5.1.13.13.11.1064',
                 'MMDB_TABLE_NAME': 'b_hlbd_patologic_reaction_types',
                 'DICT_NAME': 'Тип патологической реакции для сбора аллергоанамнеза',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_PARENT_ID': 'PARENT',
                                                    'UF_ID_SNOMED': 'SCTID'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_patologic_reactions',                               # 37
                 'OID': '1.2.643.5.1.13.13.11.1063',
                 'MMDB_TABLE_NAME': 'b_hlbd_patologic_reactions',
                 'DICT_NAME': 'Основные клинические проявления патологических реакций для сбора аллергоанамнеза',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_ID_SNOMED': 'SCTID',
                                                    'UF_SYN': 'NAME_SYN'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_units',                                             # 38
                 'OID': '1.2.643.5.1.13.13.11.1461',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_units',
                 'DICT_NAME': 'Медицинские учреждения',
                 'COLUMN_MATCHING': pickle.dumps({'UF_OID': 'oid',
                                                    'UF_OLD_OID': 'oldOid',
                                                    'UF_NAME_FULL': 'nameFull',
                                                    'UF_NAME_SHORT': 'nameShort',
                                                    'UF_PARENT_ID': 'parentId',
                                                    'UF_MED_SUBJECT_ID': 'medicalSubjectId',
                                                    'UF_MED_SUBJECT_NAME': 'medicalSubjectName',
                                                    'UF_INN': 'inn',
                                                    'UF_KPP': 'kpp',
                                                    'UF_OGRN': 'ogrn',
                                                    'UF_REGION_ID': 'regionId',
                                                    'UF_REGION_NAME': 'regionName',
                                                    'UF_ORG_TYPE': 'organizationType',
                                                    'UF_MO_DEPT_NAME': 'moDeptName',
                                                    'UF_FOUNDER': 'founder',
                                                    'UF_DEL_DATE': 'deleteDate',
                                                    'UF_DEL_REASON': 'deleteReason',
                                                    'UF_CREATE_DATE': 'createDate',
                                                    'UF_MODIFY_DATE': 'modifyDate',
                                                    'UF_MO_LEVEL': 'moLevel',
                                                    'UF_MO_AGENCY_KIND': 'moAgencyKind',
                                                    'UF_PROF_AGENCY_KIND': 'profileAgencyKind',
                                                    'UF_POST_INDEX': 'postIndex',
                                                    'UF_CAD_NUMBER': 'cadastralNumber',
                                                    'UF_LAT': 'latitude',
                                                    'UF_LONG': 'longtitude',
                                                    'UF_FIAS_VERSION': 'fiasVersion',
                                                    'UF_AOID_AREA': 'aoidArea',
                                                    'UF_AOID_STREET': 'aoidStreet',
                                                    'UF_HOUSE_ID': 'houseid',
                                                    'UF_ADDR_REGION_ID': 'addrRegionId',
                                                    'UF_ADDR_REGION_NAME': 'addrRegionName',
                                                    'UF_TERRITORY_CODE': 'territoryCode',
                                                    'UF_IS_FEDERAL_CITY': 'isFederalCity',
                                                    'UF_AREA_NAME': 'areaName',
                                                    'UF_PREFIX_AREA': 'prefixArea',
                                                    'UF_STREET_NAME': 'streetName',
                                                    'UF_PREFIX_STREET': 'prefixStreet',
                                                    'UF_HOUSE': 'house',
                                                    'UF_BUILDING': 'building',
                                                    'UF_STRUCT': 'struct'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'id'})},
                {'NSI_TABLE_NAME': 'nsi_professional_study_status',                         # 39
                 'OID': '1.2.643.5.1.13.13.11.1074',
                 'MMDB_TABLE_NAME': 'b_hlbd_prof_study_status',
                 'DICT_NAME': 'Специальности высшего и среднего профобразования',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PARENT',
                                                    'UF_NAME': 'NAME',
                                                    'UF_ORDER_ID': 'ORDER_ID',
                                                    'UF_STUDY_ID': 'TYPE',
                                                    'UF_MEDICAL_EMP': 'MED',
                                                    'UF_ACTUAL_BIT': 'REL',
                                                    'UF_END_DATE': 'DATEOUT'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_relation_types',                                    # 40
                 'OID': '1.2.643.5.1.13.13.11.1021',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_relation_types',
                 'DICT_NAME': 'Тип родственной связи',
                 'COLUMN_MATCHING': pickle.dumps({'UF_RELATION_NAME': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_rf_subjects',                                       # 41
                 'OID': '1.2.643.5.1.13.13.99.2.186',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_rf_subjects',
                 'DICT_NAME': 'Субъекты РФ',
                 'COLUMN_MATCHING': pickle.dumps({'UF_ID_AREA': 'TERR_KOD',
                                                    'UF_AREA_NAME': 'TERR_NAME',
                                                    'UF_PARENT_ID': 'KOD_FO',
                                                    'UF_DATE_START': 'DATE_BEGIN',
                                                    'UF_DATE_STOP': 'DATE_END',
                                                    'UF_SORT_ORDER': 'S_KEY_SORT',
                                                    'UF_OIV': 'ORGON_ISP_VLASTI',
                                                    'UF_OKATO': 'OKATO'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_study_owner',                                       # 42
                 'OID': '1.2.643.5.1.13.13.99.2.250',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_study_owner',
                 'DICT_NAME': 'Заказчик целевого обучения',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PARENT_ID',
                                                    'UF_OWNER_NAME': 'customer',
                                                    'UF_OWNER_ID': 'customer_code',
                                                    'UF_LOCATION': 'customer_county'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_surgery_types',                                     # 43
                 'OID': '1.2.643.5.1.13.13.11.1359',
                 'MMDB_TABLE_NAME': 'b_hlbd_surgery_types',
                 'DICT_NAME': 'Группы хирургических операций, проводимых в стационаре',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PARENT',
                                                    'UF_NAME': 'NAME',
                                                    'UF_ID_FORM14': 'CODE_F14'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'CODE'})},
                {'NSI_TABLE_NAME': 'nsi_tuberculosis_housing',                              # 44
                 'OID': '1.2.643.5.1.13.13.99.2.69',
                 'MMDB_TABLE_NAME': 'b_hlbd_tuberculosis_housing',
                 'DICT_NAME': 'ФРБТ. Жилищные условия граждан, больных туберкулезом',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'housing'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_vital_parameters',                                  # 45
                 'OID': '1.2.643.5.1.13.13.99.2.262',
                 'MMDB_TABLE_NAME': 'b_hlbd_vital_parameters',
                 'DICT_NAME': 'Справочник витальных параметров',
                 'COLUMN_MATCHING': pickle.dumps({'UF_NAME': 'NAME',
                                                    'UF_UNITS': 'Unit'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_work_termination_reasons',                          # 46
                 'OID': '1.2.643.5.1.13.13.99.2.196',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_work_termination_reasons',
                 'DICT_NAME': 'Основание прекращения работы',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT_ID': 'PARENT_ID',
                                                    'UF_REASON': 'NAME'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_working_stress',                                    # 47
                 'OID': '1.2.643.5.1.13.13.11.1060',
                 'MMDB_TABLE_NAME': 'b_hlbd_working_stress',
                 'DICT_NAME': 'Профессиональные вредности для учета сигнальной информации о пациенте',
                 'COLUMN_MATCHING': pickle.dumps({'UF_ID_FACTOR_GROUP': 'GROUP',
                                                    'UF_NAME': 'NAME',
                                                    'UF_PARENT_ID': 'PARENT',
                                                    'UF_ID_SNOMED': 'SCTID'}),
                 'COLUMN_UPDATE': pickle.dumps({'ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medical_equipment_types',                           # 48
                 'OID': '1.2.643.5.1.13.13.11.1071',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medical_equipment_types',
                 'DICT_NAME': 'Перечень аппаратов и оборудования отделений (кабинетов) медицинской организации',
                 'COLUMN_MATCHING': pickle.dumps({'UF_PARENT': 'PID',
                                                    'UF_NAME': 'NAME',
                                                    'UF_REL': 'REL',
                                                    'UF_DATEOUT': 'DATEOUT',
                                                    'UF_SORT': 'SORT'}),
                 'COLUMN_UPDATE': pickle.dumps({'UF_NSI_ID': 'ID'})},
                {'NSI_TABLE_NAME': 'nsi_medical_schools_extended',                          # 49
                 'OID': '1.2.643.5.1.13.13.11.1519',
                 'MMDB_TABLE_NAME': 'b_hlbd_nsi_medical_schools_extended',
                 'DICT_NAME': 'Мед.учреждения (расширенный)',
                 'COLUMN_MATCHING': pickle.dumps({}),
                 'COLUMN_UPDATE': pickle.dumps({})},
                ]
