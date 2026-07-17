FROM bitnami/spark:3.5.0

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv

RUN ln -sf $(which python3) /opt/venv/bin/python

COPY requirements.txt /tmp/requirements.txt

RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r /tmp/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"
ENV PYSPARK_PYTHON=/opt/venv/bin/python
ENV PYSPARK_DRIVER_PYTHON=/opt/venv/bin/python

USER 1001

WORKDIR /opt/spark/work-dir
