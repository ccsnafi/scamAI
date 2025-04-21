# 🧠 Michel CASPER - Anti-Arnaque IA

> Un projet conçu pour **piéger les arnaqueurs téléphoniques** en leur faisant perdre du temps grâce à une IA vocale réaliste, crédible et... un peu trop bavarde 😄

---

## 🎯 Objectif

Développer une IA qui :
- 🗣️ écoute un escroc via micro
- 🤖 génère des réponses crédibles avec un LLM
- 🔊 répond à l’escroc avec une voix humaine synthétisée
- 🎭 joue un personnage naïf et distrait pour l’embarquer dans la discussion

---

## 🧔 Le personnage : Michel CASPER

> Michel est un homme de 45 ans, vivant à Paris, naïf, gentil, passionné de timbres, un peu lent et bavard. Il est parfait pour occuper un escroc.

---

## 🧪 Technologies utilisées

- 🎤 **Reconnaissance vocale** : Google Speech-to-Text
- 🧠 **LLM** : HuggingFace (Qwen2.5-32B)
- 🗣️ **Synthèse vocale** : Google Text-to-Speech
- 🌐 **Interface web** : Flask + HTML + CSS + JS
- 🎮 **Audio playback** : pygame

---

## 🔧 Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ccsnafi/michel-casper-anti-scam.git
cd michel-casper-anti-scam
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Ajouter vos clés API

- Placez vos fichiers :
  - `private/key.json` (clé Google Cloud)
  - `private/nebius_api_key.txt` (clé HuggingFace via Nebius)

---

## 🚀 Lancer l’application web

```bash
python app.py
```

Puis aller sur : [http://localhost:5000](http://localhost:5000)

---

## 🧠 Fonctionnalités IA

- Comprend ce que dit l’arnaqueur (micro)
- Réagit en jouant un rôle crédible (LLM)
- Répond avec une voix réaliste (TTS)
- Ajoute hésitations, lapsus, répétitions
- Affiche le dialogue + bouton de téléchargement

---

## 👤 Auteur

**TENUDA-EKLOU Afi**  
Projet réalisé dans le cadre d'un exercice IA & Voix

---

## 📸 Aperçu

## 📸 Aperçu

[Voir la vidéo d'aperçu](preview.mp4)

---

## 🛡️ Avertissement

Ce projet est un **prototype à but pédagogique**.  
Il ne doit pas être utilisé pour contacter ou harceler qui que ce soit.  
Les appels doivent être simulés dans un cadre contrôlé.

---
