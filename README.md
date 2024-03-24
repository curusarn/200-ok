
## Run server & Ngrok
```sh
python always-200-ok.py

ngrok http http://localhost:8000 --domain=yoursubdomain.eu.ngrok.io
```


## Inspect traffic

- Locally: http://127.0.0.1:4040/inspect/http

- Ngrok dashboard: https://dashboard.ngrok.com/ac/observability/traffic-inspector  
