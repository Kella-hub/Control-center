# 🌐 NetDevOps Dashboard

**Automation • Observability • Security**

Dashboard NetDevOps développé en mode simulation.  
Architecture conçue dès le départ pour pouvoir se brancher plus tard sur de vrais équipements (netmiko / NAPALM).

---

## 🎯 Objectif du projet

Ce projet démontre les compétences clés d’un profil **NetDevOps Junior** :

- Python propre et modulaire (orienté objet)
- Automatisation réseau
- Infrastructure as Code (YAML)
- Observabilité (métriques + topologie)
- Sécurité et conformité
- Architecture évolutive (Drivers)

---

## 🏗️ Architecture

**Principe clé :**  
La couche `Drivers` permet de passer de la simulation à de vrais équipements sans réécrire toute l’application.

---

## ✨ Fonctionnalités

### Observabilité
- Tableau d’état des équipements en temps réel
- Graphiques CPU / Mémoire
- Historique des métriques
- Topologie réseau interactive (Pyvis)

### Automatisation
- Backup de configuration (simulation)
- Déploiement de VLAN
- Journal des actions

### Sécurité
- Score de sécurité du réseau
- Détection d’appareils non autorisés
- Contrôles de conformité

---

## 🚀 Installation

```bash
git clone https://github.com/Kella-hub/Control-center.git
cd Control-center
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py

