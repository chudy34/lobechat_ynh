#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/../scripts/_common.sh"

test_root=$(mktemp -d)
trap 'rm -rf -- "$test_root"' EXIT
export TMPDIR="$test_root/tmp"
mkdir -p "$TMPDIR" "$test_root/live"
install_dir="$test_root/live"
printf 'live environment\n' > "$install_dir/.env"
printf 'live compose\n' > "$install_dir/docker-compose.yml"

app=lobehub
postgres_password=test
rustfs_access_key=test
rustfs_secret_key=test
key_vaults_secret=test
auth_secret=test
admin_email=test@example.invalid
admin_password=test
jwks_key=""

ynh_die() { printf '%s\n' "$*" >&2; return 1; }
ynh_print_info() { :; }
write_env_file() { printf 'candidate environment\n' > "$1"; }
write_compose_file() { printf 'candidate compose\n' > "$1"; }

mock_pull_failure=1
docker() {
    if [[ "$*" == *" config --images" ]]; then
        printf 'rustfs/rc:v0.1.36\nlobehub/lobehub:2.2.18\n'
    elif [[ "$*" == *" pull" ]] && [ "$mock_pull_failure" -eq 1 ]; then
        return 1
    fi
}

if preflight_package; then
    echo "Preflight accepted a failed image pull" >&2
    exit 1
fi
test "$(cat "$install_dir/.env")" = "live environment"
test "$(cat "$install_dir/docker-compose.yml")" = "live compose"
test -z "$(ls -A "$TMPDIR")"

mock_pull_failure=0
preflight_package
test "$(cat "$install_dir/.env")" = "live environment"
test "$(cat "$install_dir/docker-compose.yml")" = "live compose"
test -z "$(ls -A "$TMPDIR")"

echo "Preflight rejects failed pulls and never changes live configuration"
