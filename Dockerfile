FROM python:3.11.3

RUN apt update && apt install -y nginx && apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/gaugeme
ENV GAUGEME_CONFIG=/root/.config/gaugeme/config.yaml

COPY requirements.txt /opt/gaugeme/requirements.txt
RUN python -m pip install -r requirements.txt --disable-pip-version-check

COPY nginx.conf /etc/nginx/nginx.conf

RUN ln -s /root/.config/gaugeme/certs/ca.public.pem /etc/ssl/certs/ca.crt
RUN ln -s /root/.config/gaugeme/certs/server.private.pem /etc/ssl/private/nginx.key
RUN ln -s /root/.config/gaugeme/certs/server.public.pem /etc/ssl/certs/nginx.crt

COPY bin /opt/gaugeme/bin
COPY src /opt/gaugeme/src

ENTRYPOINT ["/opt/gaugeme/bin/run-with-proxy"]
