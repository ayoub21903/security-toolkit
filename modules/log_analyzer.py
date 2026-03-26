"""
Module : Analyse automatique des logs système
"""

import os
import platform
import re
from collections import Counter


# Fichiers de logs selon l'OS
LOG_FILES = {
    "linux": ["/var/log/auth.log", "/var/log/syslog", "/var/log/kern.log"],
    "darwin": ["/var/log/system.log"],
    "windows": [],  # Windows utilise l'Event Viewer, pas de fichiers texte simples
}


def get_log_files():
    """Retourne les fichiers de logs disponibles sur ce système."""
    system = platform.system().lower()
    candidates = LOG_FILES.get(system, [])
    return [f for f in candidates if os.path.exists(f)]


def analyze_auth_log(filepath):
    """Analyse un fichier auth.log pour détecter les tentatives SSH."""
    failed_attempts = 0
    failed_ips = []
    successful_logins = 0

    try:
        with open(filepath, "r", errors="ignore") as f:
            for line in f:
                if "Failed password" in line or "authentication failure" in line:
                    failed_attempts += 1
                    ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                    if ip_match:
                        failed_ips.append(ip_match.group(1))
                elif "Accepted password" in line or "Accepted publickey" in line:
                    successful_logins += 1
    except PermissionError:
        return None

    ip_counter = Counter(failed_ips)
    top_attackers = ip_counter.most_common(3)

    return {
        "failed_attempts": failed_attempts,
        "successful_logins": successful_logins,
        "top_attackers": top_attackers,
    }


def analyze_logs():
    """Lance l'analyse des logs disponibles et retourne un résumé."""
    summary = []
    details = {}

    log_files = get_log_files()

    if not log_files:
        summary.append("⚠ Aucun fichier de log accessible (droits insuffisants ou Windows)")
        return {"summary": summary, "details": details}

    for filepath in log_files:
        filename = os.path.basename(filepath)

        if "auth" in filename:
            result = analyze_auth_log(filepath)
            if result is None:
                summary.append(f"⚠ {filename} : permission refusée (relance avec sudo)")
            else:
                details["auth"] = result
                if result["failed_attempts"] == 0:
                    summary.append(f"✔ Aucune tentative de connexion échouée détectée")
                else:
                    summary.append(f"⚠ {result['failed_attempts']} tentatives SSH échouées détectées")
                    if result["top_attackers"]:
                        for ip, count in result["top_attackers"]:
                            summary.append(f"    → {ip} : {count} tentatives")
                if result["successful_logins"] > 0:
                    summary.append(f"✔ {result['successful_logins']} connexion(s) SSH réussie(s)")
        else:
            summary.append(f"✔ {filename} : présent mais non analysé dans cette version")

    return {"summary": summary, "details": details}
