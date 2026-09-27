#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/../scripts/_common.sh"
data_dir=$(mktemp -d)
trap 'rm -rf -- "$data_dir"' EXIT
mkdir -p "$data_dir/postgres"
printf 'preserve me\n' > "$data_dir/postgres/PG_VERSION"
ynh_die() { return 1; }

if check_postgres_data_dir_install; then
    echo "Install accepted an existing PostgreSQL database" >&2
    exit 1
fi
test "$(cat "$data_dir/postgres/PG_VERSION")" = "preserve me"
rm "$data_dir/postgres/PG_VERSION"
check_postgres_data_dir_install
echo "Install preserves existing PostgreSQL data"
