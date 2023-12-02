# DSAM web admin
## Запуск
### Запуск как systemd service
Пример systemd файла
```systemd
[Unit]
Description=DSAM web admin api fastapi
After=syslog.target
After=network.target

[Service]
User=python
Group=python
Type=simple
WorkingDirectory=/dsam-web-admin-fastapi
ExecStart=/dsam-web-admin-fastapi/.venv/bin/uvicorn app:app --port 8000
EnvironmentFile=/dsam-web-admin-fastapi/.env
RestartSec=5
Restart=always
KillMode=control-group

[Install]
WantedBy=multi-user.target
```