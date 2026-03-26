"""
Module : Récupération automatique des infos réseau
"""

import socket
import urllib.request
import json


def get_local_ip():
    """Récupère l'IP locale de la machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Impossible à récupérer"


def get_public_ip_and_location():
    """Récupère l'IP publique et la localisation via API gratuite."""
    try:
        with urllib.request.urlopen("https://ipapi.co/json/", timeout=5) as response:
            data = json.loads(response.read().decode())
            ip = data.get("ip", "?")
            city = data.get("city", "?")
            country = data.get("country_name", "?")
            org = data.get("org", "?")
            return ip, f"{city}, {country} - {org}"
    except Exception:
        return "Non disponible", "Non disponible"


def get_network_info():
    """Retourne toutes les infos réseau de la machine."""
    local_ip = get_local_ip()
    public_ip, location = get_public_ip_and_location()
    hostname = socket.gethostname()

    return {
        "local_ip": local_ip,
        "public_ip": public_ip,
        "location": location,
        "hostname": hostname,
    }
