ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Kötelező csomagok
RUN apk add --no-cache python3 py3-pip

# Követelmények és fájlok bemásolása
COPY requirements.txt /requirements.txt
COPY main.py /main.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Python csomagok telepítése --break-system-packages kapcsolóval
RUN pip3 install --break-system-packages --no-cache-dir -r /requirements.txt

# Indítás
CMD ["/run.sh"]
