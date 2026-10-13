# Adaptive DSA Recommendation Engine

> **Tech Stack:** Python · FastAPI · PostgreSQL · Codeforces API · LeetCode GraphQL · CodeChef · AtCoder API · Bayesian Knowledge Tracing (BKT) · Elo Rating Systems · React · Vite · Tailwind CSS

An intelligent competitive programming and Data Structures & Algorithms (DSA) recommendation system that links solver profiles across **Codeforces**, **LeetCode**, **CodeChef**, and **AtCoder**, tracks topic-level cognitive mastery via **Bayesian Knowledge Tracing (BKT)** over a sliding window of recent submissions, and surfaces questions mathematically tailored to maximize solver skill growth using an **Elo-based Zone of Proximal Development (ZPD)** matching layer.

---

## 🌟 Key Features

1. **4-Platform Profile & Rating Linkage**:
   - **Codeforces**: Official API integration for handle rating, max rating, contest rank, and recent verdicts (`OK`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`).
   - **LeetCode**: GraphQL public API fetching contest rating, global ranking, and solved breakdown (Easy, Medium, Hard, and tag skill counts).
   - **CodeChef**: Profile scraper extracting current rating, star tier (e.g. 1★–7★), global rank, and total solved count.
   - **AtCoder**: Kenkoooo API integration extracting rating, highest rating, and official color tiers (Gray, Brown, Green, Cyan, Blue, Yellow, Orange, Red).

2. **Cross-Platform Solved Aggregation & Canonical Topic Taxonomy**:
   - Computes the combined total number of problems solved across all 4 platforms.
   - Normalizes diverse platform tags into 10 Canonical DSA Topics:
     1. *Dynamic Programming*
     2. *Graph Algorithms*
     3. *Trees & Binary Search Trees*
     4. *Binary Search & Two Pointers*
     5. *Greedy Algorithms*
     6. *Data Structures (Stack, Queue, Heap, DSU)*
     7. *Math & Number Theory*
     8. *Strings & Tries*
     9. *Bit Manipulation*
     10. *Backtracking & Recursion*
   - Visualizes categorized problems solved per topic via interactive bar and distribution charts.

3. **Per-Topic Bayesian Knowledge Tracing (BKT)**:
   - Implements BKT over a sliding window of the **last 20 submissions per topic**.
   - Standard 4-parameter formulation:
     - $L_0 = 0.15$ (Prior probability of knowing the skill)
     - $T = 0.10$ (Transition/learning probability between problem attempts)
     - $G = 0.15$ (Guess probability: solving without mastery)
     - $S = 0.08$ (Slip probability: failing despite mastery)
   - Posterior update after an Accepted ($k = \text{Correct}$) or Wrong-Answer ($k = \text{Incorrect}$) verdict:
     $$P(L | \text{Correct}) = \frac{P(L) \cdot (1 - S)}{P(L) \cdot (1 - S) + (1 - P(L)) \cdot G}$$
     $$P(L | \text{Incorrect}) = \frac{P(L) \cdot S}{P(L) \cdot S + (1 - P(L)) \cdot (1 - G)}$$
     $$P(L_k) = P(L | \text{Outcome}) + (1 - P(L | \text{Outcome})) \cdot T$$
   - Categorizes mastery status: *Novice* ($<35\%$), *Developing* ($35\%-59\%$), *Competent* ($60\%-79\%$), *Mastered* ($\ge 80\%$).

4. **Elo Rating & Zone of Proximal Development (ZPD) Matcher**:
   - Calculates solver expected win probability:
     $$E = \frac{1}{1 + 10^{(R_{\text{problem}} - R_{\text{user}}) / 400}}$$
   - Evaluates cognitive learning suitability using a Gaussian curve centered at the optimal challenge frontier ($\Delta_{\text{target}} = +75$ Elo):
     $$\text{ZPD\_Fit}(R_{\text{problem}}, R_{\text{user}}) = \exp\left(-\frac{(R_{\text{problem}} - (R_{\text{user}} + 75))^2}{2 \cdot 180^2}\right)$$
   - Dynamically shifts solver Elo using $K = 24$:
     $$R_{\text{new}} = R_{\text{old}} + K \cdot (\text{Actual} - \text{Expected})$$

5. **Adaptive Recommendation Ranking Engine**:
   - Behind a high-performance FastAPI endpoint (`GET /api/recommendations`), filters out all previously solved problems across all 4 platforms and fuses the BKT mastery vector with the Elo difficulty match score:
     $$\text{Composite Score} = w_{\text{zpd}} \cdot \text{ZPD\_Fit} + w_{\text{bkt}} \cdot (1 - P(L_{\text{topic}}))$$
   - Supports focus modes:
     - **Balanced ZPD**: $w_{\text{zpd}} = 0.55, w_{\text{bkt}} = 0.45$
     - **Weakness Focus**: $w_{\text{zpd}} = 0.35, w_{\text{bkt}} = 0.65$
     - **Rating Push**: $w_{\text{zpd}} = 0.75, w_{\text{bkt}} = 0.25$
   - Generates transparent explainability rationales for each problem.

6. **Interactive Sandbox & Full Web Application**:
   - JWT authentication (`/api/auth/register`, `/api/auth/login`, `/api/auth/me`).
   - Real-time verdict logger: click `[Mark AC]` or `[Mark WA]` to watch BKT and Elo adapt immediately.
   - Interactive BKT simulator sandbox to model hypothetical sequences.

---

## 🏗️ Architecture

```
DSA problem reccommender/
├── backend/
│   ├── main.py                  # FastAPI entrypoint & static mount
│   ├── config.py                # Pydantic settings & database URL
│   ├── database.py              # Async SQLAlchemy session & table init
│   ├── seed_data.py             # Problem catalog seed & Codeforces fetcher
│   ├── models/
│   │   ├── user.py              # User model with platform handles
│   │   ├── submission.py        # Submission model with verdicts & tags
│   │   ├── bkt_state.py         # TopicMasteryState model
│   │   └── problem.py           # ProblemCatalog model
│   ├── auth/
│   │   ├── security.py          # Bcrypt hashing & verification
│   │   ├── jwt.py               # JWT tokens
│   │   └── dependencies.py      # get_current_user dependency
│   ├── services/
│   │   ├── canonical_topics.py  # 10 DSA topics & tag normalizers
│   │   ├── bkt_model.py         # Bayesian Knowledge Tracing engine
│   │   ├── elo_matcher.py       # Elo ZPD matching engine
│   │   ├── ranking_engine.py    # Multi-criteria recommendation engine
│   │   └── platforms/
│   │       ├── codeforces.py    # Codeforces API client
│   │       ├── leetcode.py      # LeetCode GraphQL client
│   │       ├── codechef.py      # CodeChef profile scraper
│   │       ├── atcoder.py       # AtCoder Kenkoooo client
│   │       └── aggregator.py    # Cross-platform synchronization
│   └── routers/
│       ├── auth.py              # Register, login, update handles
│       ├── platforms.py         # Sync & aggregated stats
│       ├── bkt.py               # Mastery vector & simulation
│       ├── recommendations.py   # Adaptive problem ranking
│       └── problems.py          # Problem catalog browse & seed
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main dashboard orchestration
│   │   ├── api.js               # Axios client with JWT interceptor
│   │   └── components/
│   │       ├── Header.jsx       # Brand, unified Elo, sync controls
│   │       ├── PlatformCards.jsx# 4 platform rating cards & total solved
│   │       ├── TopicBreakdownChart.jsx # Recharts topic solve breakdown
│   │       ├── BktMasteryMatrix.jsx    # BKT mastery gauges & status
│   │       ├── RecommendationFeed.jsx  # Adaptive problem feed + verdict logger
│   │       ├── BktSimulator.jsx # Interactive algorithm sandbox
│   │       ├── AuthModal.jsx    # Login / Register modal
│   │       └── SettingsModal.jsx# Manage connected handles
├── test_engine.py               # Complete backend verification suite
├── test_learner.py              # Personalization test suite
├── start_app.py                 # Server runner script
└── requirements.txt             # Python dependencies
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.13)
- Node.js 20+

### 2. Setup Virtual Environment & Dependencies
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Python requirements
pip install -r requirements.txt
```

### 3. Database Configuration (PostgreSQL or SQLite)
By default, the application runs out-of-the-box on async SQLite (`sqlite+aiosqlite:///./dsa_adaptive.db`).

To connect to **PostgreSQL**, set your connection string in `.env` (or environment variable):
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/dsa_adaptive
```
SQLAlchemy handles PostgreSQL (`asyncpg`) seamlessly with identical schema migrations and models.

### 4. Build or Run Frontend
The frontend is already built into `frontend/dist/` and served automatically by FastAPI.

To run the frontend in Vite live reload dev mode:
```bash
cd frontend
npm run dev
```

### 5. Start the Application
Run the unified server:
```bash
python start_app.py
```
- Web Application Dashboard: **http://localhost:8000**
- Interactive Swagger API Docs: **http://localhost:8000/docs**

---

## 🧪 Running Verification Tests
Execute the automated test suite testing auth, 4-platform sync, BKT sliding window, Elo ZPD matching, and recommendation generation:
```bash
python test_engine.py
```

To test recommendation personalization for a new intermediate learner:
```bash
python test_learner.py
```

---

## 📚 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register coder with username, email, password & 4 platform handles |
| `POST` | `/api/auth/login` | Authenticate and obtain JWT Bearer token |
| `GET` | `/api/auth/me` | Fetch active user profile, handles, and overall Elo |
| `PUT` | `/api/auth/handles` | Update connected platform handles |
| `POST` | `/api/platforms/sync` | Sync Codeforces, LeetCode, CodeChef & AtCoder, update BKT |
| `GET` | `/api/platforms/stats` | Get 4 platform ratings, combined total solved, and topic breakdown |
| `GET` | `/api/bkt/mastery` | Retrieve the per-topic Bayesian Knowledge Tracing vector |
| `POST` | `/api/bkt/submit-verdict` | Log AC/WA verdict; updates BKT sliding window & Elo in real time |
| `POST` | `/api/bkt/simulate` | Sandbox endpoint to simulate hypothetical verdict streams |
| `GET` | `/api/recommendations` | Core adaptive recommendation engine endpoint |
| `GET` | `/api/problems` | Browse and filter problem catalog |
