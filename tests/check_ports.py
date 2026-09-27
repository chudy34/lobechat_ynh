#!/usr/bin/env python3
"""Verify installation rejects an occupied host port before starting Docker."""

from pathlib import Path
import socket
import subprocess


root = Path(__file__).resolve().parents[1]


def unused_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupied:
    occupied.bind(("127.0.0.1", 0))
    occupied.listen()
    blocked_port = occupied.getsockname()[1]
    other_ports = []
    while len(other_ports) < 2:
        candidate = unused_port()
        if candidate not in {blocked_port, *other_ports}:
            other_ports.append(candidate)
    shell = f"""source '{root / 'scripts/_common.sh'}'
port={blocked_port}
port_rustfs_api={other_ports[0]}
port_rustfs_console={other_ports[1]}
ynh_die() {{ return 1; }}
check_install_ports_available
"""
    result = subprocess.run(["bash", "-c", shell], text=True, capture_output=True)
    assert result.returncode != 0
    assert f"127.0.0.1:{blocked_port}" in result.stderr

result = subprocess.run(["bash", "-c", shell], text=True, capture_output=True)
assert result.returncode == 0, result.stderr
print("Install preflight detects occupied ports and accepts released ports")
