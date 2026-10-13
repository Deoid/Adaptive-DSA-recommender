import axios from 'axios';

const API_BASE = '/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 3000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('dsa_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Canonical Topics
const TOPICS = [
  'Dynamic Programming',
  'Graph Algorithms',
  'Trees & Binary Search Trees',
  'Binary Search & Two Pointers',
  'Greedy Algorithms',
  'Data Structures (Stack, Queue, Heap, DSU)',
  'Math & Number Theory',
  'Strings & Tries',
  'Bit Manipulation',
  'Backtracking & Recursion',
];

// In-Browser Problem Pool for Live Demo on GitHub Pages
const DEMO_PROBLEMS = [
  {
    id: 1,
    problem_id: '455A',
    platform: 'codeforces',
    title: 'Boredom',
    url: 'https://codeforces.com/problemset/problem/455/A',
    canonical_topic: 'Dynamic Programming',
    difficulty: 1500,
    tags: 'dp, greedy',
  },
  {
    id: 2,
    problem_id: 'coin-change',
    platform: 'leetcode',
    title: 'Coin Change',
    url: 'https://leetcode.com/problems/coin-change/',
    canonical_topic: 'Dynamic Programming',
    difficulty: 1450,
    tags: 'Dynamic Programming, BFS',
  },
  {
    id: 3,
    problem_id: '520B',
    platform: 'codeforces',
    title: 'Two Buttons',
    url: 'https://codeforces.com/problemset/problem/520/B',
    canonical_topic: 'Graph Algorithms',
    difficulty: 1400,
    tags: 'dfs, graphs, greedy',
  },
  {
    id: 4,
    problem_id: 'network-delay-time',
    platform: 'leetcode',
    title: 'Network Delay Time',
    url: 'https://leetcode.com/problems/network-delay-time/',
    canonical_topic: 'Graph Algorithms',
    difficulty: 1600,
    tags: 'Graph, Dijkstra',
  },
  {
    id: 5,
    problem_id: '580C',
    platform: 'codeforces',
    title: 'Kefa and Park',
    url: 'https://codeforces.com/problemset/problem/580/C',
    canonical_topic: 'Trees & Binary Search Trees',
    difficulty: 1500,
    tags: 'trees, dfs',
  },
  {
    id: 6,
    problem_id: 'lowest-common-ancestor',
    platform: 'leetcode',
    title: 'Lowest Common Ancestor of a Binary Tree',
    url: 'https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/',
    canonical_topic: 'Trees & Binary Search Trees',
    difficulty: 1450,
    tags: 'Tree, DFS',
  },
  {
    id: 7,
    problem_id: '279B',
    platform: 'codeforces',
    title: 'Books',
    url: 'https://codeforces.com/problemset/problem/279/B',
    canonical_topic: 'Binary Search & Two Pointers',
    difficulty: 1400,
    tags: 'binary search, two pointers',
  },
  {
    id: 8,
    problem_id: 'container-with-most-water',
    platform: 'leetcode',
    title: 'Container With Most Water',
    url: 'https://leetcode.com/problems/container-with-most-water/',
    canonical_topic: 'Binary Search & Two Pointers',
    difficulty: 1400,
    tags: 'Two Pointers, Greedy',
  },
  {
    id: 9,
    problem_id: '158B',
    platform: 'codeforces',
    title: 'Taxi',
    url: 'https://codeforces.com/problemset/problem/158/B',
    canonical_topic: 'Greedy Algorithms',
    difficulty: 1100,
    tags: 'greedy',
  },
  {
    id: 10,
    problem_id: 'trapping-rain-water',
    platform: 'leetcode',
    title: 'Trapping Rain Water',
    url: 'https://leetcode.com/problems/trapping-rain-water/',
    canonical_topic: 'Data Structures (Stack, Queue, Heap, DSU)',
    difficulty: 1750,
    tags: 'Monotonic Stack, Two Pointers',
  },
  {
    id: 11,
    problem_id: '230B',
    platform: 'codeforces',
    title: 'T-primes',
    url: 'https://codeforces.com/problemset/problem/230/B',
    canonical_topic: 'Math & Number Theory',
    difficulty: 1300,
    tags: 'math, number theory',
  },
  {
    id: 12,
    problem_id: 'subsets',
    platform: 'leetcode',
    title: 'Subsets',
    url: 'https://leetcode.com/problems/subsets/',
    canonical_topic: 'Backtracking & Recursion',
    difficulty: 1250,
    tags: 'Backtracking, Array',
  },
];

// In-Browser BKT and Elo Engine for GitHub Pages Live Demo
class ClientEngine {
  constructor() {
    this.user = {
      id: 1,
      username: 'tourist_coder',
      email: 'tourist@example.com',
      codeforces_handle: 'hardikjha0011',
      leetcode_handle: 'hardikjha0011',
      codechef_handle: 'hardikjha0011',
      atcoder_handle: 'hardikjha0011',
      overall_elo: 1375,
    };

    const TOPIC_INITIAL_DATA = {
      'Math & Number Theory': { mastery: 0.74, elo: 1480, accuracy: 0.80, attempts: 44, status: 'Competent' },
      'Binary Search & Two Pointers': { mastery: 0.68, elo: 1430, accuracy: 0.75, attempts: 48, status: 'Competent' },
      'Data Structures (Stack, Queue, Heap, DSU)': { mastery: 0.58, elo: 1390, accuracy: 0.65, attempts: 51, status: 'Developing' },
      'Greedy Algorithms': { mastery: 0.52, elo: 1350, accuracy: 0.60, attempts: 38, status: 'Developing' },
      'Dynamic Programming': { mastery: 0.38, elo: 1280, accuracy: 0.45, attempts: 42, status: 'Developing' },
      'Graph Algorithms': { mastery: 0.41, elo: 1290, accuracy: 0.48, attempts: 35, status: 'Developing' },
      'Trees & Binary Search Trees': { mastery: 0.46, elo: 1320, accuracy: 0.52, attempts: 29, status: 'Developing' },
      'Bit Manipulation': { mastery: 0.44, elo: 1310, accuracy: 0.50, attempts: 24, status: 'Developing' },
      'Backtracking & Recursion': { mastery: 0.34, elo: 1260, accuracy: 0.42, attempts: 30, status: 'Novice' },
      'Strings & Tries': { mastery: 0.28, elo: 1240, accuracy: 0.35, attempts: 26, status: 'Novice' },
    };

    this.masteryMap = {};
    TOPICS.forEach((t) => {
      const init = TOPIC_INITIAL_DATA[t] || { mastery: 0.45, elo: 1320, accuracy: 0.5, attempts: 20, status: 'Developing' };
      this.masteryMap[t] = {
        topic: t,
        mastery_probability: init.mastery,
        topic_elo: init.elo,
        status: init.status,
        total_attempts: init.attempts,
        recent_accuracy: init.accuracy,
      };
    });
  }

  stepBkt(prior, isCorrect) {
    const p = Math.max(0.01, Math.min(0.99, prior));
    const S = 0.08, G = 0.15, T = 0.10;
    let post;
    if (isCorrect) {
      const num = p * (1 - S);
      post = num / (num + (1 - p) * G);
    } else {
      const num = p * S;
      post = num / (num + (1 - p) * (1 - G));
    }
    return Math.max(0.01, Math.min(0.99, post + (1 - post) * T));
  }

  calcZpd(userElo, problemDifficulty) {
    const ideal = userElo + 75;
    const diff = problemDifficulty - ideal;
    return Math.exp(- (diff * diff) / (2 * 180 * 180));
  }

  expectedWin(userElo, diff) {
    return 1 / (1 + Math.pow(10, (diff - userElo) / 400));
  }

  rankProblems(mode = 'balanced', targetTopic = null, platform = null) {
    let list = DEMO_PROBLEMS;
    if (targetTopic) list = list.filter((p) => p.canonical_topic === targetTopic);
    if (platform && platform !== 'all') list = list.filter((p) => p.platform === platform);

    return list.map((p) => {
      const m = this.masteryMap[p.canonical_topic] || { mastery_probability: 0.25, topic_elo: 1350 };
      const zpd = this.calcZpd(m.topic_elo, p.difficulty);
      const e = this.expectedWin(m.topic_elo, p.difficulty);
      const growth = 1 - m.mastery_probability;

      let score = 0.55 * zpd + 0.45 * growth;
      if (mode === 'weakness_focus') score = 0.35 * zpd + 0.65 * growth;
      if (mode === 'rating_push') score = 0.75 * zpd + 0.25 * growth;

      const delta = p.difficulty - m.topic_elo;
      return {
        ...p,
        composite_score: Math.round(score * 1000) / 1000,
        zpd_score: Math.round(zpd * 1000) / 1000,
        mastery_probability: m.mastery_probability,
        expected_solve_probability: Math.round(e * 100) / 100,
        rating_delta: delta,
        difficulty_tier: delta > 250 ? 'Extremely Challenging' : delta >= 50 ? 'Optimal Growth Zone' : 'Reinforcement',
        recommendation_rationale: `Topic mastery is ${Math.round(m.mastery_probability * 100)}% (${p.canonical_topic}). Problem rating ${p.difficulty} (${delta >= 0 ? '+' : ''}${delta} Elo) offers an estimated ${Math.round(e * 100)}% win rate in your optimal growth zone.`,
      };
    }).sort((a, b) => b.composite_score - a.composite_score);
  }
}

const clientEngine = new ClientEngine();

// Dual-mode API (FastAPI Backend + GitHub Pages Live Demo Fallback)
export const authApi = {
  login: async (username, password) => {
    try {
      return await api.post('/auth/login', { username_or_email: username, password });
    } catch {
      localStorage.setItem('dsa_token', 'demo_token');
      return { data: { access_token: 'demo_token', user: clientEngine.user } };
    }
  },
  register: async (payload) => {
    try {
      return await api.post('/auth/register', payload);
    } catch {
      localStorage.setItem('dsa_token', 'demo_token');
      clientEngine.user = { ...clientEngine.user, ...payload };
      return { data: { access_token: 'demo_token', user: clientEngine.user } };
    }
  },
  getMe: async () => {
    try {
      return await api.get('/auth/me');
    } catch {
      return { data: clientEngine.user };
    }
  },
  updateHandles: async (payload) => {
    try {
      return await api.put('/auth/handles', payload);
    } catch {
      clientEngine.user = { ...clientEngine.user, ...payload };
      return { data: { status: 'success', handles: payload } };
    }
  },
};

export const platformApi = {
  sync: async () => {
    try {
      return await api.post('/platforms/sync');
    } catch {
      return { data: { status: 'success', data: await platformApi.getStats().then(r => r.data) } };
    }
  },
  getStats: async () => {
    try {
      return await api.get('/platforms/stats');
    } catch {
      return {
        data: {
          ratings: {
            codeforces: { handle: clientEngine.user.codeforces_handle, rating: 946, rank: 'newbie', maxRating: 1050 },
            leetcode: { handle: clientEngine.user.leetcode_handle, rating: 1540, global_ranking: 45000, easy: 45, medium: 52, hard: 5 },
            codechef: { handle: clientEngine.user.codechef_handle, rating: 1368, stars: '1★', global_rank: 51000 },
            atcoder: { handle: clientEngine.user.atcoder_handle, rating: 112, tier: 'Gray', highest_rating: 112 },
            overall_unified_elo: 1375,
          },
          problems_solved: {
            combined_total: 386,
            platform_breakdown: { codeforces: 140, leetcode: 102, codechef: 131, atcoder: 13 },
            topic_breakdown: {
              'Dynamic Programming': 42,
              'Graph Algorithms': 35,
              'Trees & Binary Search Trees': 29,
              'Binary Search & Two Pointers': 48,
              'Greedy Algorithms': 38,
              'Data Structures (Stack, Queue, Heap, DSU)': 51,
              'Math & Number Theory': 44,
              'Strings & Tries': 26,
              'Bit Manipulation': 24,
              'Backtracking & Recursion': 30,
            },
          },
        },
      };
    }
  },
};

export const bktApi = {
  getMastery: async () => {
    try {
      return await api.get('/bkt/mastery');
    } catch {
      return { data: { user_id: 1, overall_elo: 1375, topics: Object.values(clientEngine.masteryMap) } };
    }
  },
  submitVerdict: async (payload) => {
    try {
      return await api.post('/bkt/submit-verdict', payload);
    } catch {
      const current = clientEngine.masteryMap[payload.topic];
      if (current) {
        current.mastery_probability = Math.round(clientEngine.stepBkt(current.mastery_probability, payload.is_accepted) * 100) / 100;
        current.topic_elo += payload.is_accepted ? 18 : -14;
        current.status = current.mastery_probability >= 0.8 ? 'Mastered' : current.mastery_probability >= 0.6 ? 'Competent' : current.mastery_probability >= 0.35 ? 'Developing' : 'Novice';
      }
      return { data: { status: 'success' } };
    }
  },
  simulate: async (payload) => {
    try {
      return await api.post('/bkt/simulate', payload);
    } catch {
      let p = payload.initial_p_l;
      const history = [p];
      payload.verdicts.forEach(v => {
        p = clientEngine.stepBkt(p, v);
        history.push(p);
      });
      return {
        data: {
          bkt_result: { mastery_probability: p, status: p >= 0.8 ? 'Mastered' : 'Developing', history },
          final_elo: payload.user_elo + 45,
          zpd_evaluation: { difficulty_tier: 'Optimal Growth Zone' },
        },
      };
    }
  },
};

export const recApi = {
  getRecommendations: async (params) => {
    try {
      return await api.get('/recommendations', { params });
    } catch {
      return {
        data: {
          user_id: 1,
          recommendations: clientEngine.rankProblems(params?.mode, params?.topic, params?.platform),
        },
      };
    }
  },
};
