# Gaugeme — Your Personal Metrics Ingested & Visualized

## What is Gaugeme?

TODO: Image

A personal dashboard that allows you to track Key Performance Indicators (KPIs) of your life, such as time spend on unproductive websites.

The dashboard is accessed using a web browser for easy display on a tablet or TV.

## Getting Started

Host requirements:
* python3
* openssl
* docker

First, generate client and server certificates:

```bash
# Requires `python3` and `openssl` executables
./scripts/generate-certs certs/

docker build . -t gaugeme
docker run \
    --volume $(pwd)/certs/ca.public.pem:/root/.config/gaugeme/certs/ca.public.pem \
    --volume $(pwd)/certs/server.private.pem:/root/.config/gaugeme/certs/server.private.pem \
    --volume $(pwd)/certs/server.public.pem:/root/.config/gaugeme/certs/server.public.pem \
    --volume $(pwd)/config.example.yaml:/root/.config/gaugeme/config.yaml \
    --publish 44300:443 \
    --name gaugeme \
    gaugeme
```

Lastly, load the client certificates in your browser to access the dashboard.

## Security: Built-in TLS management and Proxy

Gaugeme is intended to be exposed on the internet.
To do this safely, web clients must present a TLS client certificate when connecting to the server.
This makes the connection similarly safe to an SSH or VPN connection, where the client authenticate using a private key.

TLS connections are terminated by an Nginx web server running inside the Docker container.
For ease of use, the container can generate all certificates automatically.
