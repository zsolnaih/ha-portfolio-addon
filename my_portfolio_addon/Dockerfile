ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Necessary packages
RUN apk add --no-cache python3 py3-pip python3-virtualenv

# Copy
COPY requirements.txt /requirements.txt
COPY main.py /main.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Creating venv
RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r /requirements.txt

# Start
CMD ["/run.sh"]
