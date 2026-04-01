"""
Module : Scan des ports ouverts sur la propre machine
3 modes : rapide, complet, personnalisé
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ports courants avec leur service associé
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    1723: "PPTP",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9200: "Elasticsearch",
    27017: "MongoDB",
}

# Ports sensibles (risque élevé s'ils sont ouverts)
SENSITIVE_PORTS = {23, 135, 139, 445, 1433, 3389, 5900}


def get_service(port):
    if port in COMMON_PORTS:
        return COMMON_PORTS[port]
    try:
        return socket.getservbyport(port)
    except Exception:
        return "Inconnu"


def check_port(port, timeout=0.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex(("127.0.0.1", port))
        s.close()
        return result == 0
    except Exception:
        return False


def scan_ports(ports, timeout=0.5, workers=100, show_progress=False):
    open_ports = {}
    total = len(ports)
    done = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(check_port, port, timeout): port for port in ports}
        for future in as_completed(futures):
            port = futures[future]
            done += 1
            if future.result():
                open_ports[port] = get_service(port)

            if show_progress and done % 500 == 0:
                pct = int(done / total * 100)
                filled = int(pct / 5)
                bar = f"{'█' * filled}{'░' * (20 - filled)}"
                sys.stdout.write(f"\r  [{bar}] {pct:3d}%  ({done}/{total} ports)")
                sys.stdout.flush()

    if show_progress:
        sys.stdout.write(f"\r  [{'█' * 20}] 100%  ({total}/{total} ports)\n")
        sys.stdout.flush()

    return dict(sorted(open_ports.items()))


def scan_quick():
    """Scan rapide : ports courants uniquement."""
    return scan_ports(list(COMMON_PORTS.keys()), timeout=0.5, workers=50)


def scan_full():
    """Scan complet : tous les ports 1-65535."""
    return scan_ports(list(range(1, 65536)), timeout=0.3, workers=300, show_progress=True)


def scan_custom(start, end):
    """Scan personnalisé : plage choisie par l'utilisateur."""
    ports = list(range(start, end + 1))
    return scan_ports(ports, timeout=0.4, workers=100, show_progress=len(ports) > 500)


def is_sensitive(port):
    return port in SENSITIVE_PORTS