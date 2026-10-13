# 🚀 ADR: Adaptive DSA Recommendation Engine

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Ready-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TailwindCSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
</p>

---

## 📌 Overview

**ADR (Adaptive DSA Recommender)** is an intelligent competitive programming and Data Structures & Algorithms learning engine. 

Instead of solving random problems or grinding without direction, ADR:
1. **Aggregates your real coder profiles across 4 major platforms**: **Codeforces**, **LeetCode**, **CodeChef**, and **AtCoder**.
2. **Models your topic-by-topic mastery** in real time using **Bayesian Knowledge Tracing (BKT)** over a sliding window of your recent submissions.
3. **Identifies your Zone of Proximal Development (ZPD)** via continuous **Elo-based difficulty matching**, surfacing the exact problems that maximize skill growth while preventing cognitive overload or boredom.

---

## ⚡ Key Highlights

### 1. 🌐 Unified 4-Platform Profile Linkage
- **Codeforces**: Official API integration tracking current rating, max rating, contest rank, and verdicts (`OK`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`).
- **LeetCode**: GraphQL public API tracking contest rating, global ranking, and problem breakdown across Easy, Medium, and Hard.
- **CodeChef**: Profile scraper extracting live rating, stars tier (1★ to 7★), global rank, and total solved problems.
- **AtCoder**: Kenkoooo API integration extracting algorithm rating, highest rating, and official color tiers.
- **Combined Aggregation**: Calculates your unified solve count across all 4 platforms and categorizes problems into **10 Canonical DSA Topics**.

### 2. 🧠 Per-Topic Bayesian Knowledge Tracing (BKT)
Maintains an evolving probability vector $P(L_t) \in [0.0, 1.0]$ for each DSA topic over a **sliding window of the last 20 attempts**:
- **$L_0 = 0.15$**: Prior probability of skill mastery.
- **$T = 0.10$**: Learning transition probability between attempts.
- **$G = 0.15$**: Guess probability (solving without complete mastery).
- **$S = 0.08$**: Slip probability (failing due to execution mistakes despite mastery).
- Updates dynamically after every **Accepted (AC)** or **Wrong Answer (WA)** verdict.
- Automatically classifies topic mastery into:
  - 🔴 **Novice** ($< 35\%$)
  - 🟡 **Developing** ($35\% - 59\%$)
  - 🔵 **Competent** ($60\% - 79\%$)
  - 🟢 **Mastered** ($\ge 80\%$)

### 3. 🎯 Elo-Based Zone of Proximal Development (ZPD) Matcher
- Computes expected solve probability using logistic Elo curves:
  ```text
  E = 1 / (1 + 10 ^ ((Rating_problem - Rating_user) / 400))
  ```
- Evaluates growth potential using a Gaussian suitability distribution centered at the optimal challenge point ($\Delta = +75$ Elo points above current solver rating):
  ```text
  ZPD_Fit = exp(- (Rating_problem - (Rating_user + 75))^2 / (2 * 180^2))
  ```
- Updates solver Elo dynamically with $K = 24$ after every attempt:
  ```text
  Rating_new = Rating_old + K * (Actual - Expected)
  ```

### 4. 📈 Adaptive Recommendation Ranking Engine
Fuses BKT topic growth room with Elo difficulty fit to rank candidate problems:
```text
Composite Score = (w_zpd * ZPD_Fit) + (w_bkt * (1 - P(L_topic)))
```
Supports multiple adaptive training modes:
- **Balanced Growth (Default)**: $55\%$ Elo ZPD fit + $45\%$ BKT mastery growth.
- **Weakness Focus**: $35\%$ Elo ZPD fit + $65\%$ BKT mastery growth (prioritizes low-mastery topics).
- **Rating Push**: $75\%$ Elo ZPD fit + $25\%$ BKT mastery growth (challenges your rating frontier).
- **Transparent Explainability**: Every problem displays a clear rationale explaining *why* it was surfaced.

---

## 🗺️ 10 Canonical DSA Topics

Tags across Codeforces, LeetCode, CodeChef, and AtCoder are normalized into:
1. **Dynamic Programming**
2. **Graph Algorithms**
3. **Trees & Binary Search Trees**
4. **Binary Search & Two Pointers**
5. **Greedy Algorithms**
6. **Data Structures (Stack, Queue, Heap, DSU)**
7. **Math & Number Theory**
8. **Strings & Tries**
9. **Bit Manipulation**
10. **Backtracking & Recursion**

---

## 🏗️ System Architecture

```text
ADR Project
├── backend/
│   ├── main.py                  # FastAPI server & SPA static handler
│   ├── config.py                # Environment & settings
│   ├── database.py              # Async SQLAlchemy engine & session maker
│   ├── seed_data.py             # Curated problem catalog seeder
│   ├── models/                  # User, UserSubmission, TopicMasteryState, ProblemCatalog
│   ├── auth/                    # JWT authentication & bcrypt security
│   ├── services/
│   │   ├── bkt_model.py         # Bayesian Knowledge Tracing engine
│   │   ├── elo_matcher.py       # Elo ZPD matching layer
│   │   ├── ranking_engine.py    # Multi-criteria recommendation engine
│   │   ├── canonical_topics.py  # 10 DSA topics taxonomy & tag mapper
│   │   └── platforms/           # Codeforces, LeetCode, CodeChef, AtCoder connectors
│   └── routers/                 # Auth, Platforms, BKT, Recommendations, Problems
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main dashboard orchestration
│   │   ├── api.js               # Axios client with JWT interceptor
│   │   └── components/          # PlatformCards, TopicChart, MasteryMatrix, RecFeed
│   ├── dist/                    # Production built frontend assets
│   └── vite.config.js           # Vite build & Tailwind configuration
├── start_app.py                 # Unified 1-click startup script
├── test_engine.py               # Complete test verification suite
└── requirements.txt             # Python dependencies
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Node.js 20+**

### 2. Setup Virtual Environment
```powershell
# Clone the repository
git clone https://github.com/Deoid/Adaptive-DSA-recommender.git
cd Adaptive-DSA-recommender

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Database Configuration
By default, the application runs with **zero setup** on asynchronous SQLite (`sqlite+aiosqlite:///./dsa_adaptive.db`).

To switch to **PostgreSQL**, simply add your connection string to `.env`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/dsa_adaptive
SECRET_KEY=your-secret-key-change-in-production
```

### 4. Launch the Application
Run the unified launcher:
```powershell
python start_app.py
```
- 🌐 **Web Dashboard:** [http://localhost:8000](http://localhost:8000)
- 📖 **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Automated Tests

Run the full end-to-end verification test suite:
```powershell
python test_engine.py
```
Tests authentication, multi-platform sync, BKT sliding-window updates, Elo ZPD calculations, and recommendations ranking.

---

## 📚 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register user with platform handles |
| `POST` | `/api/auth/login` | Authenticate user and issue JWT token |
| `GET` | `/api/auth/me` | Fetch active profile and ratings |
| `PUT` | `/api/auth/handles` | Update connected platform handles |
| `POST` | `/api/platforms/sync` | Sync data across CF, LC, CC, AC & update BKT |
| `GET` | `/api/platforms/stats` | Get combined ratings, solves, and topic distribution |
| `GET` | `/api/bkt/mastery` | Retrieve current BKT mastery vector $P(L_t)$ |
| `POST` | `/api/bkt/submit-verdict` | Log problem verdict (AC/WA) and update skill state |
| `GET` | `/api/recommendations` | Get personalized adaptive DSA recommendations |
| `GET` | `/api/problems` | Search and filter the catalog problem pool |

---

## 📄 License
MIT License. Built for competitive programmers, students, and engineers preparing for technical interviews.
