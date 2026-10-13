# 🚀 ADR — Adaptive DSA Recommendation Engine

<p align="center">
  <b>Personalized Competitive Programming & DSA Growth Engine Powered by Bayesian Knowledge Tracing & Elo Systems</b>
</p>

<p align="center">
  <a href="https://deoid.github.io/Adaptive-DSA-recommender/">
    <img src="https://img.shields.io/badge/🚀_LAUNCH_LIVE_WEB_APP-CLICK_HERE-indigo?style=for-the-badge&logo=rocket" alt="Live App" />
  </a>
</p>

<p align="center">
  <a href="https://deoid.github.io/Adaptive-DSA-recommender/"><b>👉 Open Live Product in Your Browser (No Installation Needed)</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Codeforces-API_Integrated-blue?style=flat-square&logo=codeforces" />
  <img src="https://img.shields.io/badge/LeetCode-GraphQL_Linked-FFA116?style=flat-square&logo=leetcode" />
  <img src="https://img.shields.io/badge/CodeChef-Live_Sync-5B4638?style=flat-square&logo=codechef" />
  <img src="https://img.shields.io/badge/AtCoder-Kenkoooo_API-black?style=flat-square" />
  <img src="https://img.shields.io/badge/Model-Bayesian_Knowledge_Tracing-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Matcher-Elo_ZPD_System-emerald?style=flat-square" />
</p>

---

## 💡 The Problem with Traditional Problem Grinding

Most competitive programmers and software engineers grind problems in one of two ways:
- **Random Practice**: Solving arbitrary problems without knowing whether they address real skill deficiencies.
- **Plateau / Frustration Trap**: Picking problems that are either **too trivial** (yielding zero cognitive growth) or **excessively difficult** (leading to cognitive overload and wasted hours).

**ADR solves this.** It acts as an autonomous AI coach that monitors your real problem submissions across platforms, calculates your topic mastery mathematically, and surfaces the exact problem you should solve next to maximize your rate of improvement.

---

## 🌟 What ADR Does

### 1. 🌐 Unified 4-Platform Profile Aggregator
ADR connects directly to your coder identities across 4 major competitive programming platforms:
- **Codeforces**: Pulls live contest ratings, ranks, and submission histories with verdicts (`OK`, `WRONG_ANSWER`, `TIME_LIMIT_EXCEEDED`).
- **LeetCode**: Queries public GraphQL for contest ratings, global rankings, and Easy/Medium/Hard problem distributions.
- **CodeChef**: Extracts official ratings, star tiers (1★ to 7★), global ranks, and total solved problems.
- **AtCoder**: Integrates with the Kenkoooo API for algorithm rating, highest rating, and official color tiers.
- **Combined Intelligence**: Aggregates your total solved problems into a single cross-platform count and normalizes all problem tags into **10 Canonical DSA Topics**.

---

### 2. 🧠 Per-Topic Bayesian Knowledge Tracing (BKT)
Traditional platforms only track an overall rating. ADR tracks an evolving skill probability vector $P(L_t) \in [0\%, 100\%]$ across every DSA domain using Bayesian Knowledge Tracing over a sliding window of your **last 20 submissions per topic**:

- **Initial Mastery Prior ($L_0 = 0.15$)**: Baseline probability of knowing a topic before focused practice.
- **Skill Transition Probability ($T = 0.10$)**: Rate of acquiring conceptual mastery after each problem attempt.
- **Guess Probability ($G = 0.15$)**: Likelihood of solving a problem without complete underlying mastery.
- **Slip Probability ($S = 0.08$)**: Likelihood of a wrong answer due to minor bugs despite mastering the algorithm.

Every time you submit an **Accepted (AC)** or **Wrong Answer (WA)**, ADR recalculates your posterior mastery probability and classifies your skill:
- 🔴 **Novice** ($< 35\%$)
- 🟡 **Developing** ($35\% - 59\%$)
- 🔵 **Competent** ($60\% - 79\%$)
- 🟢 **Mastered** ($\ge 80\%$)

---

### 3. 🎯 Elo Zone of Proximal Development (ZPD) Matcher
Cognitive psychology demonstrates that maximum learning occurs in the **Zone of Proximal Development (ZPD)** — tasks that are slightly beyond current ability but achievable with effort.

ADR models this mathematically:
- **Logistic Win Expectancy**:
  ```text
  E = 1 / (1 + 10 ^ ((Difficulty_problem - Skill_user) / 400))
  ```
- **Gaussian Growth Suitability**:
  Scores highest when a problem is positioned at the optimal challenge delta ($\Delta = +75$ Elo points above current skill level):
  ```text
  ZPD_Fit = exp(- (Difficulty_problem - (Skill_user + 75))^2 / (2 * 180^2))
  ```

---

### 4. 📈 Recommendation Ranking Engine
The recommendation engine eliminates solved questions across all 4 platforms and scores candidate problems using a composite objective function:
```text
Composite Score = (w_zpd * ZPD_Fit) + (w_bkt * (1 - P(L_topic)))
```

#### Custom Training Modes:
- ⚖️ **Balanced ZPD (Default)**: Harmonious blend of optimal difficulty matching ($55\%$) and topic weakness training ($45\%$).
- 🛡️ **Weakness Focus**: Targets domains where your Bayesian mastery is lowest ($65\%$ BKT weight).
- 🚀 **Rating Push**: Focuses on higher-difficulty problems to push your rating ceiling ($75\%$ ZPD weight).
- 🔍 **Domain Filter**: Train on a specific topic (e.g. *Dynamic Programming*, *Graph Algorithms*, or *Trees*).
- 💬 **Explainability Rationale**: Every recommended problem features a transparent explanation of why it was chosen, its predicted solve rate, and its expected learning yield.

---

## 🗂️ 10 Canonical DSA Topics

Tags across all platforms are unified into 10 fundamental computer science domains:
1. **Dynamic Programming** (Knapsack, LIS, Interval DP, Tree DP, Bitmask DP)
2. **Graph Algorithms** (Dijkstra, BFS/DFS, Shortest Paths, Topological Sort, Bipartite)
3. **Trees & Binary Search Trees** (LCA, Tree Traversals, Segment Trees, Fenwick Trees)
4. **Binary Search & Two Pointers** (Monotonic predicates, Sliding Window)
5. **Greedy Algorithms** (Interval Scheduling, Huffman, Exchange Arguments)
6. **Data Structures** (Monotonic Stack, Priority Queue / Heap, Disjoint Set Union)
7. **Math & Number Theory** (Modular Arithmetic, Primes, Sieve, Combinatorics)
8. **Strings & Tries** (KMP, Z-Algorithm, Trie Prefix Trees, Suffix Structures)
9. **Bit Manipulation** (Bitwise masks, Submask iteration, XOR tricks)
10. **Backtracking & Recursion** (N-Queens, Permutations, Subsets, Branch and Bound)

---

## 🖥️ Live Product Experience

The web application provides an all-in-one developer workspace:

| Dashboard View | What It Delivers |
|---|---|
| **Platform Cards** | Live ratings and official badges for Codeforces, LeetCode, CodeChef, and AtCoder |
| **Combined Solves Counter** | Real-time aggregate count of unique problems solved across the competitive ecosystem |
| **Topic Distribution Chart** | Interactive breakdown of solves categorized across the 10 canonical DSA domains |
| **BKT Mastery Matrix** | Visual progress gauges showing your real-time $P(\text{Mastery})$ and topic Elo |
| **Adaptive Problem Feed** | Surfaced questions with direct **Solve on Platform ↗** links and instant **[AC]** / **[WA]** verdict logging |

---

## 🔗 Try It Live

You can launch and explore the product directly in your browser:
### 🚀 **[https://deoid.github.io/Adaptive-DSA-recommender/](https://deoid.github.io/Adaptive-DSA-recommender/)**

---

<p align="center">
  <b>ADR: Adaptive DSA Recommendation Engine</b><br>
  <i>Built for competitive programmers, computer science students, and engineers striving for peak algorithm mastery.</i>
</p>
