# 🧩 Vue Dashboard + Flask API

Ce projet est un **dashboard modulaire** développé avec **Vue 3** côté frontend et **Flask** côté backend. Il permet d'ajouter dynamiquement des widgets tels que :

- ✅ **TodoList** (avec stockage persistant)
- 🧮 **Calculatrice** (expressions avec décimales)
- 🌤 **Météo** (requêtes à l'API OpenWeatherMap)

Chaque widget est **déplaçable, fermable, personnalisable**, et le dashboard est **persisté** (ordre, type, config) via un fichier JSON côté serveur.

---

## ⚙️ Installation

### 🐍 Backend (Flask)

1. Va dans le dossier `backend` :

   ```bash
   cd backend
   ```

2. Installe les dépendances :

   ```bash
   pip install flask flask-cors requests
   ```

3. (Optionnel) Crée un fichier widgets.json et todos.json vides :
   ```json
   []
   ```
4. Lance le serveur :
   ```bash
   python app.py
   ```

📌 L'API tourne sur http://localhost:5000

### 🌐 Frontend (Vue 3)

1. Va dans le dossier frontend :

   ```bash
   cd frontend
   ```

2. Installe les dépendances :

   ```bash
   npm install
   ```

3. Lance le projet :
   ```bash
   npm run dev
   ```

📌 Le frontend tourne sur http://localhost:5173 (ou autre port Vite)

### 🌦 Configuration de l’API météo (Weather Widget)

1. Crée un compte sur https://openweathermap.org

2. Obtiens une clé API

3. Dans backend/app.py, remplace :
   ```python
   OPENWEATHER_API_KEY = 'TA_CLE_API_ICI'
   ```

### 💾 Persistance

    - Tous les widgets sont sauvegardés dans backend/widgets.json
    - Chaque todo dans todos.json (backend partagé)
    - Le backend expose /api/widgets et /api/todos

### ✨ À venir

    - Sauvegarde par utilisateur
    - Authentification / sessions
    ...
