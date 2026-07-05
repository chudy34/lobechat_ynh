#!/bin/bash

set_lobechat_base_path() {
    base_path=""
    if [ "$path" != "/" ]; then
        base_path="$path"
    fi
}

build_lobechat() {
    set_lobechat_base_path

    pushd "$install_dir"
        ynh_exec_as_app corepack enable
        ynh_exec_as_app corepack use pnpm
        ynh_exec_as_app pnpm install --frozen-lockfile
        ynh_exec_as_app env NEXT_PUBLIC_BASE_PATH="$base_path" npm run build:docker
        ynh_exec_as_app cp -R public .next/standalone/public
        ynh_exec_as_app mkdir -p .next/standalone/.next
        ynh_exec_as_app cp -R .next/static .next/standalone/.next/static
    popd
}

configure_lobechat_env() {
    set_lobechat_base_path

    mkdir -p "/etc/$app"
    ynh_config_add --template="env" --destination="/etc/$app/env"
    chmod 600 "/etc/$app/env"
    chown "root:$app" "/etc/$app/env"
}
