FROM python:3.8.10-alpine
RUN apk add --no-cache tzdata
RUN apk add --no-cache gcc libc-dev
ENV TZ=America/New_York
ENV MQTT_HOST=localhost
ENV MQTT_PORT=1883
ENV MQTT_USER=rhasspy
ENV MQTT_PASSWORD=password

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN addgroup rhasspy-app \
    && adduser rhasspy-app --disabled-password --no-create-home --ingroup rhasspy-app \
    && chown -R rhasspy-app /app
USER rhasspy-app

COPY hermes-app-time.py /app 
RUN mkdir config
COPY config/responses.txt /app/config

CMD [ "sh", "-c", "python3 hermes-app-time.py --host ${MQTT_HOST} --username ${MQTT_USER} --password ${MQTT_PASSWORD} --port ${MQTT_PORT}" ]