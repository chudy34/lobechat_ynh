#!/usr/bin/env python3
"""Run the packaged RustFS initializer against a disposable RustFS server."""

import os
from pathlib import Path
import subprocess
import tempfile


root = Path(__file__).resolve().parents[1]
app = "lobehub-ci"

with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    workspace.chmod(0o755)

    helper = (root / "scripts/_common.sh").read_text()
    policy = helper.split("<< 'BUCKET_EOF'\n", 1)[1].split("\nBUCKET_EOF", 1)[0]
    (workspace / "bucket.config.json").write_text(policy + "\n")

    compose = (root / "conf/docker-compose.yml").read_text()
    for source, replacement in {
        "__APP__": app,
        "__INSTALL_DIR__": directory,
        "__DATA_DIR__": directory,
        "__PORT__": "23210",
        "__PORT_RUSTFS_API__": "29000",
        "__PORT_RUSTFS_CONSOLE__": "29001",
    }.items():
        compose = compose.replace(source, replacement)
    # Keep database files inside a disposable Docker volume. RustFS writes
    # files as its own UID, which the CI runner cannot remove from /tmp.
    compose = compose.replace(f"- {directory}/rustfs:/data", "- rustfs-test-data:/data")
    compose += "\nvolumes:\n  rustfs-test-data:\n"
    compose_file = workspace / "docker-compose.yml"
    compose_file.write_text(compose)

    environment = os.environ.copy()
    environment.update(
        {
            "LOBE_DB_NAME": "lobehub",
            "POSTGRES_PASSWORD": "test-password",
            "RUSTFS_ACCESS_KEY": "test-access-key",
            "RUSTFS_SECRET_KEY": "test-secret-key-12345",
            "RUSTFS_LOBE_BUCKET": "lobe",
            "KEY_VAULTS_SECRET": "test",
            "AUTH_SECRET": "test",
            "S3_PUBLIC_DOMAIN": "https://example.invalid/s3",
            "APP_URL": "https://example.invalid",
        }
    )
    (workspace / ".env").write_text("\n".join(f"{key}={environment[key]}" for key in (
        "LOBE_DB_NAME", "POSTGRES_PASSWORD", "RUSTFS_ACCESS_KEY", "RUSTFS_SECRET_KEY",
        "RUSTFS_LOBE_BUCKET", "KEY_VAULTS_SECRET", "AUTH_SECRET", "S3_PUBLIC_DOMAIN", "APP_URL",
    )) + "\n")
    command = ["docker", "compose", "--project-name", app, "--file", str(compose_file)]
    try:
        subprocess.run(command + ["up", "-d", "rustfs-init"], env=environment, check=True, timeout=240)
        result = subprocess.run(["docker", "wait", f"{app}-rustfs-init"], text=True, capture_output=True, check=True, timeout=180)
        if result.stdout.strip() != "0":
            raise RuntimeError(f"RustFS initializer exited with {result.stdout.strip()}")
        print("RustFS bucket initialization completed successfully")
    except Exception:
        subprocess.run(command + ["ps", "-a"], env=environment, check=False)
        subprocess.run(command + ["logs", "--tail", "100", "rustfs", "rustfs-init"], env=environment, check=False)
        raise
    finally:
        subprocess.run(command + ["down", "--volumes", "--timeout", "10"], env=environment, check=False)
