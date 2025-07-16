ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Kötelező csomagok + Python modulok
COPY requirements.txt /
RUN apk add --no-cache python3 py3-pip && pip3 install --no-cache-dir -r /requirements.txt

COPY run.sh /run.sh
COPY main.py /main.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
