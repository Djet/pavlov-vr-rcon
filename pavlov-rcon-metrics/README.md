## Pavlov rcon metrics

Grafana stack with pavlov-vr-exporter

exit rcon config file:

config.yaml
```
---
servers:
  HAGUENAU:
    host: 10.31.21.2
    port: 15001
    password: "PaSsWord"

```

```
docker-compose build
docker-compose up -d
```

Open http://127.0.0.1:3000, credentials: admin/admin

Saved dashboards:

http://127.0.0.1:3000/d/dgHc0jDVz

