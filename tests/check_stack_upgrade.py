#!/usr/bin/env python3
"""Exercise the packaged Compose stack and a disposable LobeHub image upgrade."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import tomllib
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--from-image", help="Existing LobeHub image to upgrade from")
args = parser.parse_args()

version = tomllib.loads((ROOT / "manifest.toml").read_text())["version"].split("~", 1)[0]
target_image = f"lobehub/lobehub:{version}"
if args.from_image and not re.fullmatch(r"lobehub/lobehub:[0-9]+\.[0-9]+\.[0-9]+", args.from_image):
    parser.error("--from-image must be a stable lobehub/lobehub version")

project = "lobehub-stack-ci"
app_url = "http://127.0.0.1:23210"


def run(command, *, env, timeout=300):
    return subprocess.run(command, env=env, text=True, capture_output=True, check=True, timeout=timeout)


def wait_for_http(compose, env, stage):
    deadline = time.monotonic() + 600
    last_error = "no response"
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(app_url + "/", timeout=8) as response:
                body = response.read(4096)
                if response.status < 400 and body:
                    print(f"{stage}: HTTP {response.status}, {len(body)} response bytes")
                    return
                last_error = f"HTTP {response.status} with empty body"
        except (OSError, urllib.error.HTTPError) as error:
            last_error = str(error)
        lobe = subprocess.run(compose + ["ps", "-q", "lobe"], env=env, text=True, capture_output=True)
        if lobe.stdout.strip():
            state = subprocess.run(["docker", "inspect", "--format", "{{.State.Status}}", lobe.stdout.strip()], text=True, capture_output=True)
            if state.stdout.strip() in {"exited", "restarting", "dead"}:
                raise RuntimeError(f"{stage}: LobeHub container is {state.stdout.strip()}; last HTTP error: {last_error}")
        time.sleep(5)
    raise TimeoutError(f"{stage}: LobeHub did not respond within 10 minutes: {last_error}")


with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    workspace.chmod(0o755)
    (workspace / "searxng").mkdir()
    (workspace / "searxng/settings.yml").write_text(
        'use_default_settings: true\nserver:\n  secret_key: "ci-test-secret"\n  limiter: false\n'
        'search:\n  formats:\n    - html\n    - json\n'
    )
    common = (ROOT / "scripts/_common.sh").read_text()
    policy = common.split("<< 'BUCKET_EOF'\n", 1)[1].split("\nBUCKET_EOF", 1)[0]
    (workspace / "bucket.config.json").write_text(policy + "\n")

    compose_text = (ROOT / "conf/docker-compose.yml").read_text()
    for source, replacement in {
        "__APP__": project,
        "__INSTALL_DIR__": directory,
        "__DATA_DIR__": directory,
        "__PORT__": "23210",
        "__PORT_RUSTFS_API__": "29010",
        "__PORT_RUSTFS_CONSOLE__": "29011",
    }.items():
        compose_text = compose_text.replace(source, replacement)
    for service in ("postgres", "redis", "rustfs"):
        compose_text = compose_text.replace(f"- {directory}/{service}:/", f"- ci-{service}:/")
    compose_text += "\nvolumes:\n  ci-postgres:\n  ci-redis:\n  ci-rustfs:\n"
    assert f"image: {target_image}" in compose_text
    if args.from_image:
        compose_text = compose_text.replace(f"image: {target_image}", f"image: {args.from_image}", 1)

    compose_file = workspace / "docker-compose.yml"
    compose_file.write_text(compose_text)
    environment = os.environ.copy()
    environment.update({
        "LOBE_DB_NAME": "lobehub",
        "POSTGRES_PASSWORD": "ci-test-postgres-password",
        "RUSTFS_ACCESS_KEY": "ci-test-access-key",
        "RUSTFS_SECRET_KEY": "ci-test-secret-key-12345",
        "RUSTFS_LOBE_BUCKET": "lobe",
        "KEY_VAULTS_SECRET": "0123456789abcdef0123456789abcdef",
        "AUTH_SECRET": "0123456789abcdef0123456789abcdef",
        "S3_PUBLIC_DOMAIN": "http://127.0.0.1:29010",
        "APP_URL": app_url,
    })
    (workspace / ".env").write_text("\n".join(
        f"{key}={environment[key]}" for key in (
            "LOBE_DB_NAME", "POSTGRES_PASSWORD", "RUSTFS_ACCESS_KEY", "RUSTFS_SECRET_KEY",
            "RUSTFS_LOBE_BUCKET", "KEY_VAULTS_SECRET", "AUTH_SECRET", "S3_PUBLIC_DOMAIN", "APP_URL",
        )
    ) + "\n")
    compose = ["docker", "compose", "--project-name", project, "--file", str(compose_file)]

    try:
        run(compose + ["config", "--quiet"], env=environment)
        run(compose + ["up", "-d", "lobe"], env=environment, timeout=900)
        wait_for_http(compose, environment, "Initial install")
        init = run(["docker", "inspect", "--format", "{{.State.ExitCode}}", f"{project}-rustfs-init"], env=environment)
        assert init.stdout.strip() == "0", "RustFS bucket initialization did not succeed"

        sql = (
            "CREATE TABLE IF NOT EXISTS public.ci_upgrade_guard (value text PRIMARY KEY); "
            "INSERT INTO public.ci_upgrade_guard VALUES ('preserved') ON CONFLICT DO NOTHING;"
        )
        run(compose + ["exec", "-T", "postgresql", "psql", "-v", "ON_ERROR_STOP=1", "-U", "postgres", "-d", "lobehub", "-c", sql], env=environment)

        if args.from_image and args.from_image != target_image:
            compose_file.write_text(compose_text.replace(f"image: {args.from_image}", f"image: {target_image}", 1))
            run(compose + ["up", "-d", "--no-deps", "lobe"], env=environment, timeout=900)
            wait_for_http(compose, environment, "Image upgrade")

        running_image = run(["docker", "inspect", "--format", "{{.Config.Image}}", f"{project}-lobe"], env=environment)
        assert running_image.stdout.strip() == target_image, "The tested LobeHub image is not running"
        marker = run(compose + ["exec", "-T", "postgresql", "psql", "-At", "-U", "postgres", "-d", "lobehub", "-c", "SELECT value FROM public.ci_upgrade_guard;"], env=environment)
        assert marker.stdout.strip() == "preserved", "Database marker was lost during the upgrade"
        print("Full stack responds and PostgreSQL data is preserved")
    except Exception:
        subprocess.run(compose + ["ps", "-a"], env=environment, check=False)
        subprocess.run(compose + ["logs", "--tail", "100", "postgresql", "rustfs", "rustfs-init", "lobe"], env=environment, check=False)
        raise
    finally:
        subprocess.run(compose + ["down", "--volumes", "--timeout", "10"], env=environment, check=False)
