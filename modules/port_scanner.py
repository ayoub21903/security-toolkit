"""
Module : Scan des ports ouverts sur la propre machine
"""

import socket
from concurrent.futures import ThreadPoolExecutor

# Ports courants à scanner
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
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def check_port(port, timeout=0.5):
    """Vérifie si un port est ouvert sur localhost."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex(("127.0.0.1", port))
        s.close()
        return result == 0
    except Exception:
        return False


def scan_own_ports():
    """Scanne les ports courants sur la machine locale."""
    open_ports = {}

    def scan(port):
        if check_port(port):
            open_ports[port] = COMMON_PORTS[port]

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(scan, COMMON_PORTS.keys())

    return dict(sorted(open_ports.items()))
