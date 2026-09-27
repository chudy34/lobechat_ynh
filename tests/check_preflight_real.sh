#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
workspace=$(mktemp -d)
trap 'rm -rf -- "$workspace"' EXIT
mkdir -p "$workspace/install" "$workspace/data"
printf 'unchanged environment\n' > "$workspace/install/.env"
printf 'unchanged compose\n' > "$workspace/install/docker-compose.yml"

cd "$root/scripts"
source ./_common.sh
ynh_die() { echo "$*" >&2; return 1; }
ynh_print_info() { echo "$*"; }

app=lobehub-ci-preflight
install_dir="$workspace/install"
data_dir="$workspace/data"
port=23210
port_rustfs_api=29010
port_rustfs_console=29011
APP_URL=https://example.invalid
postgres_password=ci-postgres-password
rustfs_access_key=ci-access-key
rustfs_secret_key=ci-secret-key
key_vaults_secret=0123456789abcdef0123456789abcdef
auth_secret=0123456789abcdef0123456789abcdef
admin_email=ci@example.invalid
admin_password=ci-password
jwks_key=""

preflight_package
test "$(cat "$install_dir/.env")" = "unchanged environment"
test "$(cat "$install_dir/docker-compose.yml")" = "unchanged compose"
echo "Real Docker preflight passed without changing live files"
