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
from modules.port_scanner import scan_quick, scan_full, scan_custom, is_sensitive
from modules.network_scan import scan_local_network
from modules.log_analyzer import analyze_logs
from modules.report import save_report

import time


def choose_scan_mode():
    """Affiche le menu de choix du mode de scan."""
    print()
    print(f"  {C.BOLD}Mode de scan des ports :{C.RESET}")
    print(f"  {C.GRAY}╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌{C.RESET}")
    print(f"  {C.GREEN}[1]{C.RESET}  Rapide       — {C.GRAY}ports courants uniquement (~2s){C.RESET}")
    print(f"  {C.YELLOW}[2]{C.RESET}  Complet      — {C.GRAY}tous les ports 1-65535 (~2 min){C.RESET}")
    print(f"  {C.CYAN}[3]{C.RESET}  Personnalisé — {C.GRAY}tu choisis la plage{C.RESET}")
    print()

    while True:
        choix = input(f"  {C.BOLD}→ {C.RESET}").strip()
        if choix == "1":
            return "quick", None, None
        elif choix == "2":
            return "full", None, None
        elif choix == "3":
            print()
            try:
                start = int(input(f"  {C.BOLD}Port de départ  → {C.RESET}").strip())
                end   = int(input(f"  {C.BOLD}Port de fin     → {C.RESET}").strip())
                if 1 <= start <= end <= 65535:
                    return "custom", start, end
                else:
                    warn("Plage invalide (1-65535)")
            except ValueError:
                warn("Entre des nombres valides")
        else:
            warn("Choisis 1, 2 ou 3")


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

    ok("Hostname",     net_info["hostname"])
    ok("IP locale",    net_info["local_ip"])
    ok("IP publique",  net_info["public_ip"])
    ok("Localisation", net_info["location"])

    # ── Ports ouverts ────────────────────────────────────────────────────────
    section("Scan des ports", "◈")

    mode, start, end = choose_scan_mode()
    print()

    if mode == "quick":
        spinner("Scan rapide en cours...", duration=0.5)
        open_ports = scan_quick()
    elif mode == "full":
        print(f"  {C.YELLOW}⚠{C.RESET}  Scan complet — cela peut prendre 1-2 minutes...\n")
        open_ports = scan_full()
        print()
    else:
        print(f"  {C.CYAN}◈{C.RESET}  Scan de {start} à {end}...\n")
        open_ports = scan_custom(start, end)
        print()

    report_data["open_ports"] = open_ports

    if open_ports:
        sensitive_found = []
        for port, service in open_ports.items():
            sensitive = is_sensitive(port)
            port_line(port, service, open=True, sensitive=sensitive)
            if sensitive:
                sensitive_found.append((port, service))
        if sensitive_found:
            print()
            warn(f"{len(sensitive_found)} port(s) sensible(s) détecté(s) !")
            for port, service in sensitive_found:
                info(f"Port {port} ({service}) — risque élevé s'il est exposé")
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

    # ── Téléchargement du rapport ─────────────────────────────────────────────
    section("Rapport d'audit", "◈")

    print()
    print(f"  {C.BOLD}Voulez-vous sauvegarder le rapport ?{C.RESET}")
    print(f"  {C.GREEN}[yes]{C.RESET}  Sauvegarder le rapport")
    print(f"  {C.RED}[no]{C.RESET}   Quitter sans sauvegarder")
    print()

    while True:
        choix = input(f"  {C.BOLD}→ {C.RESET}").strip().lower()
        if choix in ("yes", "y", "oui", "o"):
            break
        elif choix in ("no", "n", "non"):
            print()
            print(f"  {C.GRAY}Rapport non sauvegardé. À bientôt !{C.RESET}")
            print()
            return
        else:
            warn("Réponds par  yes  ou  no")

    print()
    print(f"  {C.BOLD}Dans quel format ?{C.RESET}")
    print(f"  {C.GREEN}[txt]{C.RESET}  Rapport lisible (texte brut)")
    print(f"  {C.CYAN}[json]{C.RESET} Rapport structuré (JSON)")
    print(f"  {C.YELLOW}[both]{C.RESET} Les deux formats")
    print()

    while True:
        format_choix = input(f"  {C.BOLD}→ {C.RESET}").strip().lower()
        if format_choix in ("txt", "json", "both"):
            break
        else:
            warn("Réponds par  txt,  json  ou  both")

    spinner("Écriture du rapport...", duration=0.6)
    path = save_report(report_data, format=format_choix)
    print_footer(path)


if __name__ == "__main__":
    main()