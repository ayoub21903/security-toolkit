"""
Module : Scan des machines actives sur le réseau local
"""

import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor


def ping_host(ip):
    """Ping une IP et retourne True si elle répond."""
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "500", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]

    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False


def get_subnet(local_ip):
    """Génère la liste des IPs du sous-réseau /24."""
    base = ".".join(local_ip.split(".")[:3])
    return [f"{base}.{i}" for i in range(1, 255)]


def scan_local_network(local_ip):
    """Retourne les hôtes actifs sur le réseau local."""
    ips = get_subnet(local_ip)
    active_hosts = []

    def check(ip):
        if ping_host(ip):
            active_hosts.append(ip)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check, ips)

    return sorted(active_hosts, key=lambda ip: int(ip.split(".")[-1]))
