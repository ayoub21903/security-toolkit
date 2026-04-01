"""
Module : Génération du rapport d'audit
"""

import json
from datetime import datetime


def save_report(data, format="both"):
    """Sauvegarde le rapport d'audit selon le format choisi."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    saved = []

    if format in ("txt", "both"):
        txt_path = f"rapport_{timestamp}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("       SECURITY TOOLKIT - RAPPORT D'AUDIT\n")
            f.write(f"       {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")

            net = data.get("network", {})
            f.write("[ INFOS RÉSEAU ]\n")
            f.write(f"  Hostname    : {net.get('hostname', '?')}\n")
            f.write(f"  IP locale   : {net.get('local_ip', '?')}\n")
            f.write(f"  IP publique : {net.get('public_ip', '?')}\n")
            f.write(f"  Localisation: {net.get('location', '?')}\n\n")

            ports = data.get("open_ports", {})
            f.write("[ PORTS OUVERTS ]\n")
            if ports:
                for port, service in ports.items():
                    f.write(f"  Port {port} ({service})\n")
            else:
                f.write("  Aucun port ouvert détecté\n")
            f.write("\n")

            hosts = data.get("hosts", [])
            f.write("[ HÔTES ACTIFS SUR LE RÉSEAU LOCAL ]\n")
            for host in hosts:
                f.write(f"  {host}\n")
            f.write("\n")

            logs = data.get("logs", {})
            f.write("[ ANALYSE DES LOGS ]\n")
            for line in logs.get("summary", []):
                f.write(f"  {line}\n")

        saved.append(txt_path)

    if format in ("json", "both"):
        json_path = f"rapport_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        saved.append(json_path)

    return " + ".join(saved)