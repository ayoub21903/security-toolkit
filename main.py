#!/usr/bin/env python3
"""
Security Toolkit - Audit automatique de ta machine et ton réseau
"""

from modules.network_info import get_network_info
from modules.port_scanner import scan_own_ports
from modules.network_scan import scan_local_network
from modules.log_analyzer import analyze_logs
from modules.report import save_report

def print_banner():
    print("""
╔══════════════════════════════════════════╗
║        SECURITY TOOLKIT v1.0             ║
║        Audit automatique local           ║
╚══════════════════════════════════════════╝
    """)

def main():
    print_banner()
    report_data = {}

    # 1. Infos réseau
    print("[*] Récupération des infos réseau...")
    net_info = get_network_info()
    report_data["network"] = net_info
    print(f"    ✔ IP locale   : {net_info['local_ip']}")
    print(f"    ✔ IP publique : {net_info['public_ip']} ({net_info['location']})")
    print(f"    ✔ Hostname    : {net_info['hostname']}")

    # 2. Scan des ports
    print("\n[*] Scan de tes ports ouverts...")
    open_ports = scan_own_ports()
    report_data["open_ports"] = open_ports
    if open_ports:
        for port, service in open_ports.items():
            print(f"    ✔ Port {port:<6} ({service}) → OUVERT")
    else:
        print("    ✔ Aucun port ouvert détecté")

    # 3. Scan réseau local
    print("\n[*] Machines actives sur ton réseau local...")
    hosts = scan_local_network(net_info["local_ip"])
    report_data["hosts"] = hosts
    for host in hosts:
        label = "→ Toi" if host == net_info["local_ip"] else "→ Actif"
        print(f"    ✔ {host:<18} {label}")

    # 4. Analyse des logs
    print("\n[*] Analyse des logs système...")
    log_results = analyze_logs()
    report_data["logs"] = log_results
    for line in log_results["summary"]:
        print(f"    {line}")

    # 5. Sauvegarde du rapport
    print("\n[*] Génération du rapport...")
    path = save_report(report_data)
    print(f"    ✔ Rapport sauvegardé → {path}")
    print("\n[✔] Audit terminé !\n")

if __name__ == "__main__":
    main()
