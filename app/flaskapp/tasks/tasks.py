from celery import Celery
import subprocess
from flask_socketio import SocketIO
from flask import session, jsonify


class CeleryConfig:
    broker_url = 'redis://redis:6379/0'
    result_backend = 'redis://redis:6379/0'
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    enable_utc = False
    task_track_started = True


celery = Celery(__name__)
celery.config_from_object(CeleryConfig)
socket_io = SocketIO(message_queue='redis://redis:6379')


def send_message(event, namespace, room, message, taskid=None):
    socket_io.emit(event, {'msg': message, 'taskid': taskid}, namespace=namespace, room=room)


@celery.task(name='tasks.long_async_taskf')
def long_async_taskf(data):
    proc = None
    room = data['sessionid']
    namespace = data['namespace']
    taskargs = data['taskargs']
    send_message('status', namespace, room, 'Начало')
    send_message('msg',
                 namespace,
                 room,
                 f'Запущена операция {long_async_taskf.request.id}',
                 long_async_taskf.request.id)
    try:
        proc = subprocess.Popen(str('python /app/flaskapp/tasks/app_nsi.py ' + taskargs).split(' '),
                                stdout=subprocess.PIPE, shell=False)
    except subprocess.SubprocessError:
        print('Error calling process')
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        send_message('msg', namespace, room, str(line.rstrip().decode("utf-8")), long_async_taskf.request.id)
    rc = proc.poll()
    send_message('msg',
                 namespace,
                 room,
                 f'Завершена операция {long_async_taskf.request.id}',
                 long_async_taskf.request.id)
    send_message('status', namespace, room, 'End')


def long_task_start(task_args):
    data = {}
    data['sessionid'] = str(session.get('uid'))
    data['taskargs'] = task_args
    data['namespace'] = '/runAsyncTaskF'
    task = long_async_taskf.delay(data)
    return jsonify({'taskid': task.id,
                    'sessionid': data['sessionid'],
                    'taskargs': data['taskargs'],
                    'namespace': data['namespace']
                    })
