#!/usr/bin/env python3
"""Validate the rendered package Compose file without starting containers."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
VERSION = tomllib.loads((ROOT / "manifest.toml").read_text())["version"].split("~", 1)[0]

with tempfile.TemporaryDirectory() as directory:
    template = (ROOT / "conf/docker-compose.yml").read_text()
    for source, replacement in {
        "__APP__": "lobehub",
        "__INSTALL_DIR__": directory,
        "__DATA_DIR__": directory,
        "__PORT__": "3210",
        "__PORT_RUSTFS_API__": "9000",
        "__PORT_RUSTFS_CONSOLE__": "9001",
    }.items():
        template = template.replace(source, replacement)

    compose_file = Path(directory, "docker-compose.yml")
    compose_file.write_text(template)
    Path(directory, ".env").write_text("")
    environment = os.environ.copy()
    environment.update(
        {
            "LOBE_DB_NAME": "lobehub",
            "POSTGRES_PASSWORD": "test",
            "RUSTFS_ACCESS_KEY": "test",
            "RUSTFS_SECRET_KEY": "test",
            "RUSTFS_LOBE_BUCKET": "lobe",
            "KEY_VAULTS_SECRET": "test",
            "AUTH_SECRET": "test",
            "S3_PUBLIC_DOMAIN": "https://example.invalid/s3",
            "APP_URL": "https://example.invalid",
        }
    )
    result = subprocess.run(
        ["docker", "compose", "--project-name", "lobehub", "--file", str(compose_file), "config", "--format", "json"],
        env=environment,
        text=True,
        capture_output=True,
        check=True,
    )
    services = json.loads(result.stdout)["services"]
    assert services["lobe"]["image"] == f"lobehub/lobehub:{VERSION}"
    assert services["rustfs-init"]["image"] == "rustfs/rc:v0.1.36"
    assert services["rustfs-init"]["networks"] == services["rustfs"]["networks"]
    assert services["rustfs-init"]["depends_on"]["rustfs"]["condition"] == "service_healthy"
    assert services["lobe"]["depends_on"]["rustfs-init"]["condition"] == "service_completed_successfully"
    assert "minio/mc" not in result.stdout
    assert "amazon/aws-cli" not in result.stdout

print("Compose configuration and RustFS initialization dependencies are valid")
