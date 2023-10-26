from ..models.models import User
from ..tasks.tasks import long_task_start
from celery import current_app, result
from celery.result import AsyncResult
from flask_restx import Api, Resource, reqparse
from flask import request

api = Api()


def api_auth(username, password):
    try:
        user = User.query.filter_by(login=username).first()
        if user and user.check_password(password=password):
            return True
        else:
            return False
    except Exception as err:
        return {'message': 'Internal server error'}, 500


@api.route('/tasks')
class Tasks(Resource):
    def get(self):
        celery_worker = current_app.control.inspect()
        celery_dict = celery_worker.active()
        if len(list(celery_dict.values())[0]) > 0:
            task_id = list(celery_dict.values())[0][0]['id']
            if task_id:
                return {'taskid': task_id}
        else:
            return {'message': 'No running tasks founded'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('mode', required=True, help='Available modes: \'full\', \'full-diff\', \'download\', \'check\', \'update-diff\', \'update\', \'rollback\', \'download-check\'.')
        parser.add_argument('tables', required=True, help='Specify comma separated list of processing tables.')
        parser.add_argument('notify', required=True, help='Specify notification to Bitrix24: yes/no.')
        if request.content_type == 'application/json':
            args = request.get_json()
        else:
            args = parser.parse_args()
        username = args.get('username', '')
        password = args.get('password', '')
        mode = args.get('mode', '')
        tables = args.get('tables', '')
        notify = args.get('notify', '')
        if api_auth(username, password):
            return long_task_start(f'--mode {mode} --tables {tables} --notify {notify}')
        else:
            return {'message': 'Invalid credentials'}, 401


@api.route('/tasks/<taskid>')
class Task(Resource):
    def get(self, taskid):
        celery_worker = current_app.control.inspect()
        celery_dict = celery_worker.active()
        if len(list(celery_dict.values())[0]) > 0:
            task_id = list(celery_dict.values())[0][0]['id']
            if task_id == taskid:
                result = current_app.AsyncResult(taskid).state
                return {'message': f'{result}'}
            return {'message': f'No tasks with id "{taskid}" founded'}, 404
        else:
            return {'message': 'No running tasks founded'}, 404


    def delete(self, taskid):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        if request.content_type == 'application/json':
            args = request.get_json()
        else:
            args = parser.parse_args()
        username = args.get('username', '')
        password = args.get('password', '')
        if api_auth(username, password):
            celery_worker = current_app.control.inspect()
            celery_dict = celery_worker.active()
            if len(list(celery_dict.values())[0]) > 0:
                task_id = list(celery_dict.values())[0][0]['id']
                if task_id == taskid:
                    current_app.control.revoke(task_id, terminate=True)
                    return {'message': f'Tasks with id "{taskid}" stopped'}, 204
                return {'message': f'No tasks with id "{taskid}" founded'}, 404
            else:
                return {'message': 'No running tasks founded'}, 404
        else:
            return {'message': 'Invalid credentials'}, 401
