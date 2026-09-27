#!/usr/bin/env python3
"""Check that an older ParadeDB dump restores extensions in dependency order."""

from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
OLD_DUMP = """DROP EXTENSION IF EXISTS vector;
DROP EXTENSION IF EXISTS pg_search;
CREATE EXTENSION IF NOT EXISTS pg_search WITH SCHEMA paradedb;
CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;
"""

with tempfile.TemporaryDirectory() as directory:
    dump = Path(directory, "postgres_dump.sql")
    dump.write_text(OLD_DUMP)
    shell = f"""source '{ROOT / 'scripts/_common.sh'}'
ynh_print_info() {{ :; }}
docker() {{ cat; }}
app=lobehub
install_dir=/tmp
LOBE_DB_NAME=lobehub
restore_postgres "$1"
"""
    result = subprocess.run(
        ["bash", "-c", shell, "check_restore", str(dump)],
        text=True,
        capture_output=True,
        check=True,
    )
    lines = result.stdout.splitlines()
    assert lines[:4] == [
        "DROP EXTENSION IF EXISTS pg_search;",
        "DROP EXTENSION IF EXISTS vector;",
        "CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;",
        "CREATE EXTENSION IF NOT EXISTS pg_search WITH SCHEMA paradedb;",
    ]
    assert dump.read_text() == OLD_DUMP

print("PostgreSQL extension restore order is valid; saved dump is unchanged")
