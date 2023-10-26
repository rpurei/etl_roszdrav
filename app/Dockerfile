FROM python:3.8.10
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# веб-сервис
CMD python ./server.py
# командная строка
#CMD python ./flaskapp/instance/app_nsi.py --tables all --mode download --notify no