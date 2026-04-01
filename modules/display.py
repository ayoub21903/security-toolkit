"""
Module : Affichage visuel du terminal - couleurs, animations, mise en forme
"""

import sys
import time
import os


# ── Codes couleurs ANSI ─────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Couleurs texte
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    # Fonds
    BG_RED   = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE  = "\033[44m"


def enable_windows_ansi():
    """Active les couleurs ANSI sur Windows."""
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def typing_effect(text, delay=0.018):
    """Affiche le texte lettre par lettre."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def spinner(label, duration=1.2):
    """Affiche un spinner pendant une durée donnée."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  {C.CYAN}{frames[i % len(frames)]}{C.RESET}  {label}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {C.GREEN}✔{C.RESET}  {label}\n")
    sys.stdout.flush()


def progress_bar(label, steps=30, delay=0.03):
    """Affiche une barre de progression."""
    sys.stdout.write(f"  {label}\n  {C.GRAY}[{C.RESET}")
    for i in range(steps):
        time.sleep(delay)
        filled = int((i + 1) / steps * 20)
        bar = f"{C.CYAN}{'█' * filled}{C.GRAY}{'░' * (20 - filled)}{C.RESET}"
        pct = int((i + 1) / steps * 100)
        sys.stdout.write(f"\r  {C.GRAY}[{C.RESET}{bar}{C.GRAY}]{C.RESET} {C.BOLD}{pct:3d}%{C.RESET}  {label}")
        sys.stdout.flush()
    print()


def print_banner():
    """Affiche la bannière principale."""
    enable_windows_ansi()
    clear()

    banner = f"""
{C.CYAN}{C.BOLD}
  ███████╗███████╗ ██████╗    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
  ██╔════╝██╔════╝██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
  ███████╗█████╗  ██║            ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║
  ╚════██║██╔══╝  ██║            ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║
  ███████║███████╗╚██████╗       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║
  ╚══════╝╚══════╝ ╚═════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝
{C.RESET}"""

    print(banner)

    line = f"  {C.GRAY}{'─' * 72}{C.RESET}"
    print(line)
    print(f"  {C.GRAY}  v1.0  │  Audit automatique local  │  github.com/security-toolkit{C.RESET}")
    print(line)
    print()
    time.sleep(0.4)


def section(title, icon="◈"):
    """Affiche un titre de section."""
    print()
    print(f"  {C.CYAN}{C.BOLD}{icon}  {title}{C.RESET}")
    print(f"  {C.GRAY}{'╌' * 50}{C.RESET}")


def ok(label, value=""):
    """Ligne de succès."""
    if value:
        print(f"  {C.GREEN}✔{C.RESET}  {C.BOLD}{label:<16}{C.RESET}  {C.WHITE}{value}{C.RESET}")
    else:
        print(f"  {C.GREEN}✔{C.RESET}  {label}")


def warn(label):
    """Ligne d'avertissement."""
    print(f"  {C.YELLOW}⚠{C.RESET}  {label}")


def err(label):
    """Ligne d'erreur."""
    print(f"  {C.RED}✖{C.RESET}  {label}")


def info(label):
    """Ligne d'info neutre."""
    print(f"  {C.GRAY}│{C.RESET}  {C.DIM}{label}{C.RESET}")


def port_line(port, service, open=True):
    """Affiche une ligne pour un port."""
    if open:
        status = f"{C.GREEN}OUVERT{C.RESET}"
        icon = f"{C.GREEN}✔{C.RESET}"
    else:
        status = f"{C.GRAY}FERMÉ{C.RESET}"
        icon = f"{C.GRAY}✖{C.RESET}"
    print(f"  {icon}  Port {C.BOLD}{port:<6}{C.RESET}  {C.CYAN}{service:<12}{C.RESET}  {status}")


def host_line(ip, is_self=False):
    """Affiche une ligne pour un hôte réseau."""
    if is_self:
        tag = f"{C.MAGENTA}[Toi]{C.RESET}"
    else:
        tag = f"{C.GREEN}[Actif]{C.RESET}"
    print(f"  {C.GREEN}✔{C.RESET}  {C.BOLD}{ip:<18}{C.RESET}  {tag}")


def print_footer(report_path):
    """Affiche le footer final."""
    print()
    print(f"  {C.GRAY}{'─' * 72}{C.RESET}")
    print(f"  {C.GREEN}{C.BOLD}✔  Audit terminé avec succès{C.RESET}")
    print(f"  {C.GRAY}   Rapport sauvegardé → {C.RESET}{C.CYAN}{report_path}{C.RESET}")
    print(f"  {C.GRAY}{'─' * 72}{C.RESET}")
    print()
