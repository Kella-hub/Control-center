
**Point fort :**  
Grâce à la couche `Drivers`, on pourra brancher de vrais équipements plus tard **sans réécrire** le reste de l’application.

---

## ✨ Fonctionnalités

### 📊 Observabilité
- Tableau d’état des équipements en temps réel
- Graphiques CPU / Mémoire
- Historique des métriques
- Topologie réseau interactive (Pyvis)

### ⚙️ Automatisation
- Backup de configuration
- Déploiement de VLAN
- Journal des actions

### 🔒 Sécurité
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
# source venv/bin/activate     # Linux / Mac

pip install -r requirements.txt
streamlit run app.py

