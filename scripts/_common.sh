#!/bin/bash

# LobeHub v2 — Common variables
# Stack: lobehub/lobehub + paradedb/paradedb:pg17 + rustfs + redis + searxng
# No separate auth container (NextAuth built-in)

COMPOSE_PROJECT="lobehub_$app"

generate_secret() {
    openssl rand -hex 32
}

generate_password() {
    openssl rand -base64 16 | tr -dc 'A-Za-z0-9' | head -c 20
}
