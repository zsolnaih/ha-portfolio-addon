ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Kötelező csomagok
RUN apk add --no-cache python3 py3-pip

# Fájlok másolása
COPY requirements.txt /requirements.txt
COPY main.py /main.py
COPY rootfs/ / 

# Futtathatóvá tesszük a run fájlt
RUN chmod +x /etc/services.d/my_service/run

# Könyvtárak telepítése
RUN pip3 install --break-system-packages --no-cache-dir -r /requirements.txt
