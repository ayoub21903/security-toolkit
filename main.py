#!/usr/bin/env python3
"""
Security Toolkit - Audit automatique de ta machine et ton réseau
"""

from modules.display import (
    print_banner, section, ok, warn, err, info,
    port_line, host_line, print_footer,
    spinner, progress_bar, typing_effect, C
)
from modules.network_info import get_network_info
from modules.port_scanner import scan_own_ports
from modules.network_scan import scan_local_network
from modules.log_analyzer import analyze_logs
from modules.report import save_report

import time


def main():
    # ── Bannière ────────────────────────────────────────────────────────────
    print_banner()
    typing_effect(f"  {C.DIM}Initialisation de l'audit...{C.RESET}", delay=0.025)
    time.sleep(0.3)

    report_data = {}

    # ── Infos réseau ─────────────────────────────────────────────────────────
    section("Informations réseau", "◈")
    spinner("Récupération des infos réseau...", duration=1.0)

    net_info = get_network_info()
    report_data["network"] = net_info

    ok("Hostname",    net_info["hostname"])
    ok("IP locale",   net_info["local_ip"])
    ok("IP publique", net_info["public_ip"])
    ok("Localisation",net_info["location"])

    # ── Ports ouverts ────────────────────────────────────────────────────────
    section("Ports ouverts sur cette machine", "◈")
    progress_bar("Scan des ports en cours...", steps=30, delay=0.025)

    open_ports = scan_own_ports()
    report_data["open_ports"] = open_ports

    if open_ports:
        for port, service in open_ports.items():
            port_line(port, service, open=True)
    else:
        ok("Aucun port ouvert détecté")

    # ── Réseau local ─────────────────────────────────────────────────────────
    section("Machines actives sur le réseau local", "◈")
    progress_bar("Scan du réseau local...", steps=40, delay=0.04)

    hosts = scan_local_network(net_info["local_ip"])
    report_data["hosts"] = hosts

    if hosts:
        for host in hosts:
            host_line(host, is_self=(host == net_info["local_ip"]))
    else:
        warn("Aucun hôte détecté (réseau inaccessible ou droits insuffisants)")

    # ── Logs système ─────────────────────────────────────────────────────────
    section("Analyse des logs système", "◈")
    spinner("Lecture des fichiers de log...", duration=0.8)

    log_results = analyze_logs()
    report_data["logs"] = log_results

    for line in log_results["summary"]:
        stripped = line.strip()
        if stripped.startswith("✔"):
            ok(stripped[1:].strip())
        elif stripped.startswith("⚠"):
            warn(stripped[1:].strip())
        elif stripped.startswith("→"):
            info(stripped[1:].strip())
        else:
            info(stripped)

    # ── Rapport ──────────────────────────────────────────────────────────────
    section("Génération du rapport", "◈")
    spinner("Écriture du rapport...", duration=0.6)

    path = save_report(report_data)
    print_footer(path)


if __name__ == "__main__":
    main()