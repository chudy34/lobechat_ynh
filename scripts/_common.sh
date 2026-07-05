#!/bin/bash
# LobeHub — shared helpers

COMPOSE_PROJECT="lobehub_${app}"

# Docker Compose v2 binary path (installed via Docker CE official repo)
DOCKER_COMPOSE="docker compose"

gen_password() { openssl rand -base64 24 | tr -dc 'A-Za-z0-9' | head -c 28; }
gen_secret()   { openssl rand -hex 16; }

install_docker_ce() {
    # Skip if docker compose v2 is already available
    if docker compose version &>/dev/null 2>&1; then
        ynh_print_info "Docker CE with Compose v2 already installed."
        return 0
    fi

    ynh_print_info "Installing Docker CE (official repo — provides Compose v2)..."

    # Remove old conflicting packages
    for pkg in docker.io docker-compose docker-doc podman-docker containerd runc; do
        apt-get remove -y "$pkg" 2>/dev/null || true
    done

    # Add Docker's official GPG key
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/debian/gpg \
        | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg

    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/debian \
      $(lsb_release -cs) stable" \
      > /etc/apt/sources.list.d/docker.list

    apt-get update -qq
    apt-get install -y --no-install-recommends \
        docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    systemctl enable docker --quiet
    systemctl start docker

    # Verify
    docker compose version || ynh_die "Docker Compose v2 installation failed"
    ynh_print_info "Docker CE + Compose v2 installed: $(docker compose version)"
}
