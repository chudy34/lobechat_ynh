# LobeHub v2 for YunoHost

Pakiet YunoHost dla **LobeHub v2.1.38** (najnowsza wersja stabilna, marzec 2026).

## Stack

```
lobehub/lobehub:latest          ← główna aplikacja (v2.1.38)
paradedb/paradedb:latest-pg17   ← PostgreSQL 17 + pgvector + pg_search
rustfs/rustfs:latest            ← S3 object storage
redis:7-alpine                  ← cache
searxng/searxng:latest          ← web search
```

## Instalacja

```bash
# Z lokalnego katalogu
yunohost app install /ścieżka/do/lobehub_v2_ynh

# Z repozytorium git (po wgraniu)
yunohost app install https://github.com/TWOJ_USER/lobehub_ynh
```

## Uaktualnienie do najnowszego obrazu

```bash
yunohost app upgrade lobehub
```

Pobierze najnowszy `lobehub/lobehub:latest` i zrestartuje stack z zachowaniem danych.

## Backup / Restore

```bash
yunohost backup create --apps lobehub
yunohost backup restore BACKUP_NAME --apps lobehub
```

## Porty (wewnętrzne, za nginx)

| Port | Usługa |
|------|--------|
| `$port` | LobeHub app |
| `$port_rustfs_api` | RustFS S3 API |
| `$port_rustfs_console` | RustFS Console |

## Linki

- [LobeHub docs](https://lobehub.com/docs/self-hosting/platform/docker-compose)
- [GitHub v2](https://github.com/lobehub/lobehub)
- [Releases](https://github.com/lobehub/lobehub/releases)
