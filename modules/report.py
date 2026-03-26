"""
Module : Génération du rapport d'audit
"""

import json
from datetime import datetime


def save_report(data):
    """Sauvegarde le rapport d'audit en JSON et en .txt lisible."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    txt_path = f"rapport_{timestamp}.txt"
    json_path = f"rapport_{timestamp}.json"

    # Rapport texte lisible
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("       SECURITY TOOLKIT - RAPPORT D'AUDIT\n")
        f.write(f"       {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")

        # Réseau
        net = data.get("network", {})
        f.write("[ INFOS RÉSEAU ]\n")
        f.write(f"  Hostname    : {net.get('hostname', '?')}\n")
        f.write(f"  IP locale   : {net.get('local_ip', '?')}\n")
        f.write(f"  IP publique : {net.get('public_ip', '?')}\n")
        f.write(f"  Localisation: {net.get('location', '?')}\n\n")

        # Ports ouverts
        ports = data.get("open_ports", {})
        f.write("[ PORTS OUVERTS ]\n")
        if ports:
            for port, service in ports.items():
                f.write(f"  Port {port} ({service})\n")
        else:
            f.write("  Aucun port ouvert détecté\n")
        f.write("\n")

        # Hôtes réseau
        hosts = data.get("hosts", [])
        f.write("[ HÔTES ACTIFS SUR LE RÉSEAU LOCAL ]\n")
        for host in hosts:
            f.write(f"  {host}\n")
        f.write("\n")

        # Logs
        logs = data.get("logs", {})
        f.write("[ ANALYSE DES LOGS ]\n")
        for line in logs.get("summary", []):
            f.write(f"  {line}\n")

    # Rapport JSON (pour exploitation future)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    return txt_path
