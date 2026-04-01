# security-toolkit

## 🛠️ Introduction

`security-toolkit` est un mini-projet Python de diagnostic réseau et d’analyse de sécurité. Ce README est un tutoriel pas-à-pas pour installer, utiliser et étendre l’outil.

## 📁 Architecture du projet

- `main.py` : point d’entrée principal
- `modules/log_analyzer.py` : analyse de logs
- `modules/network_info.py` : informations réseau (IP, interfaces, etc.)
- `modules/network_scan.py` : scan réseau / découverte d’hôtes
- `modules/port_scanner.py` : scan de ports (TCP)
- `modules/report.py` : génération de rapport

---

## 🚀 Installation

1. Cloner le repo :

   ```bash
   git clone https://github.com/ayoub21903/security-toolkit.git
   cd security-toolkit
   ```

2. Créer un environnement Python :

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Installer les dépendances (s’il y en a) :

   ```bash
   pip install -U pip
   pip install -r requirements.txt  # si fichier présent
   ```

4. Vérifier la version de Python :

   ```bash
   python --version
   ```

---

## ▶️ Exécution de base

Le script principal s’exécute avec :

```bash
python main.py
```

Il doit appeler les modules du dossier `modules` et produire des sorties console + rapport.

---

## 🧩 Modules détaillés

### `modules/log_analyzer.py`
- Parse des fichiers de log
- Recherche de modèles (IP suspectes, erreurs critiques)
- Exemple d’usage :

```python
from modules.log_analyzer import LogAnalyzer
an = LogAnalyzer('logs/app.log')
findings = an.analyze()
print(findings)
```

### `modules/network_info.py`
- Affiche l’interface active, adresse IP locale, passerelle, DNS
- Exemple :

```python
from modules.network_info import NetworkInfo
ni = NetworkInfo()
print(ni.get_summary())
```

### `modules/network_scan.py`
- Scan de réseau (ICMP ou TCP)
- Découverte d’hôtes en ligne

```python
from modules.network_scan import NetworkScanner
sc = NetworkScanner('192.168.1.0/24')
hosts = sc.scan()
print(hosts)
```

### `modules/port_scanner.py`
- Scan de ports TCP
- Exemple :

```python
from modules.port_scanner import PortScanner
ps = PortScanner('192.168.1.100', ports=[22,80,443])
open_ports = ps.scan()
print(open_ports)
```

### `modules/report.py`
- Génère rapport texte/JSON
- Exemple :

```python
from modules.report import Report
r = Report('report.txt')
r.add_section('Résumé', 'OK')
r.save()
```
```

---

## 🛡️ Cas d’usage / workflow

1. Lancer un scan réseau
2. Scanner les ports des hôtes découverts
3. Analyser les logs pour corrélation
4. Générer un rapport consolidé

---

## ✨ Développement & tests

- Ajouter un module sous `modules/`
- Mettre à jour ou créer des tests (si structure de tests absente, ajouter `tests/test_*.py`)
- Exécuter:

```bash
pytest -q
```

---

## 📌 Conseils utiles

- Sous Linux, exécuter les scans avec des droits root pour ICMP et ports <1024
- Penser à respecter l’éthique : scanner seulement ce dont vous avez l’autorisation

---

## 📦 Contribution

1. Fork + clone
2. Nouvelle branche
3. PR avec description claire

---

## 📄 Licence

Aucune licence précisée. Ajouter un fichier `LICENSE` pour clarifier
