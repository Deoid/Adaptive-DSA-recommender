import React, { useState } from 'react';
import {
  ExternalLink,
  Target,
  Sparkles,
  TrendingUp,
  CheckCircle,
  XCircle,
  HelpCircle,
  Filter,
  Zap,
} from 'lucide-react';

export default function RecommendationFeed({
  recommendations,
  loading,
  mode,
  setMode,
  selectedTopic,
  setSelectedTopic,
  selectedPlatform,
  setSelectedPlatform,
  topicsList,
  onSubmitVerdict,
}) {
  const [submittingId, setSubmittingId] = useState(null);

  const handleVerdict = async (problem, isAccepted) => {
    setSubmittingId(`${problem.platform}:${problem.problem_id}`);
    try {
      await onSubmitVerdict({
        topic: problem.canonical_topic,
        problem_id: problem.problem_id,
        problem_title: problem.title,
        platform: problem.platform,
        difficulty: problem.difficulty,
        is_accepted: isAccepted,
      });
    } finally {
      setSubmittingId(null);
    }
  };

  const getTierBadge = (tier) => {
    switch (tier) {
      case 'Optimal Growth Zone':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Reinforcement':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Extremely Challenging':
        return 'bg-purple-500/10 text-purple-400 border-purple-500/30';
      default:
        return 'bg-slate-500/10 text-slate-400 border-slate-500/30';
    }
  };

  const getPlatformBadge = (platform) => {
    switch (platform.toLowerCase()) {
      case 'codeforces':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'leetcode':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'codechef':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
      case 'atcoder':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div
      id="recommendations-section"
      className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6 scroll-mt-24"
    >
      {/* Header & Controls */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white">
              Adaptive DSA Problem Recommendations
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Surfacing problems based on Bayesian Knowledge Tracing topic weakness and Elo Zone of Proximal Development.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Mode Selector */}
          <div className="flex items-center bg-slate-950 border border-slate-800 rounded-lg p-1 text-xs">
            <button
              onClick={() => setMode('balanced')}
              className={`px-3 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                mode === 'balanced'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Balanced ZPD
            </button>
            <button
              onClick={() => setMode('weakness_focus')}
              className={`px-3 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                mode === 'weakness_focus'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Weakness Focus
            </button>
            <button
              onClick={() => setMode('rating_push')}
              className={`px-3 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                mode === 'rating_push'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Rating Push
            </button>
          </div>

          {/* Topic Dropdown */}
          <select
            value={selectedTopic || ''}
            onChange={(e) => setSelectedTopic(e.target.value || null)}
            className="bg-slate-950 border border-slate-800 text-slate-300 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Topics</option>
            {(topicsList || []).map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>

          {/* Platform Dropdown */}
          <select
            value={selectedPlatform || ''}
            onChange={(e) => setSelectedPlatform(e.target.value || null)}
            className="bg-slate-950 border border-slate-800 text-slate-300 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Platforms</option>
            <option value="codeforces">Codeforces</option>
            <option value="leetcode">LeetCode</option>
            <option value="atcoder">AtCoder</option>
            <option value="codechef">CodeChef</option>
          </select>
        </div>
      </div>

      {/* Active Training Filter Banner */}
      {selectedTopic && (
        <div className="flex items-center justify-between p-3.5 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-xs shadow-inner">
          <div className="flex items-center gap-2 text-indigo-200">
            <span className="flex h-2 w-2 rounded-full bg-indigo-400 animate-ping" />
            <span>
              Training Mode Active: Surfacing optimal growth questions for{' '}
              <strong className="text-white font-semibold underline underline-offset-2">
                {selectedTopic}
              </strong>
            </span>
          </div>
          <button
            onClick={() => setSelectedTopic(null)}
            className="text-xs text-slate-400 hover:text-white px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-800 border border-slate-700 transition-colors cursor-pointer"
          >
            Clear Filter & Show All Topics &times;
          </button>
        </div>
      )}

      {/* Recommendations List */}
      {loading ? (
        <div className="py-16 text-center text-slate-500 text-sm animate-pulse">
          Evaluating Bayesian skill curves and matching problem difficulty...
        </div>
      ) : recommendations?.length === 0 ? (
        <div className="py-12 text-center text-slate-500 text-sm">
          No unsolved problems found matching your current filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((p) => {
            const isSubmitting = submittingId === `${p.platform}:${p.problem_id}`;

            return (
              <div
                key={`${p.platform}:${p.problem_id}`}
                className="bg-slate-950/80 border border-slate-800/90 hover:border-slate-700/90 rounded-xl p-5 transition-all shadow-md flex flex-col justify-between group"
              >
                <div>
                  {/* Top Badges */}
                  <div className="flex items-center justify-between gap-2 mb-2.5">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getPlatformBadge(
                          p.platform
                        )}`}
                      >
                        {p.platform}
                      </span>
                      <span className="text-xs font-mono font-bold text-white bg-slate-800/80 px-2 py-0.5 rounded">
                        Elo {p.difficulty}
                      </span>
                    </div>

                    <span
                      className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full border ${getTierBadge(
                        p.difficulty_tier
                      )}`}
                    >
                      {p.difficulty_tier}
                    </span>
                  </div>

                  {/* Title & Link */}
                  <div className="mb-2">
                    <a
                      href={p.url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-base font-semibold text-white group-hover:text-indigo-400 transition-colors inline-flex items-center gap-1.5"
                    >
                      <span>{p.title}</span>
                      <ExternalLink className="w-3.5 h-3.5 opacity-60 group-hover:opacity-100" />
                    </a>
                    <span className="text-xs text-slate-400 block mt-0.5">
                      Domain: <strong className="text-slate-300 font-normal">{p.canonical_topic}</strong>
                    </span>
                  </div>

                  {/* Explainability Rationale */}
                  <div className="bg-slate-900/90 border border-slate-800/80 rounded-lg p-3 my-3 text-xs space-y-1.5">
                    <div className="flex items-center justify-between text-slate-400 font-mono text-[11px]">
                      <span>Growth Score: <strong className="text-indigo-300 font-bold">{p.composite_score}</strong></span>
                      <span>Win Chance: <strong className="text-emerald-300 font-bold">{Math.round(p.expected_solve_probability * 100)}%</strong></span>
                      <span>Topic Mastery: <strong className="text-amber-300 font-bold">{Math.round(p.mastery_probability * 100)}%</strong></span>
                    </div>
                    <p className="text-slate-300 text-[11.5px] leading-relaxed">
                      {p.recommendation_rationale}
                    </p>
                  </div>
                </div>

                {/* Bottom Actions */}
                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-3">
                  <a
                    href={p.url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3 py-1.5 rounded-lg bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 hover:text-white border border-indigo-500/40 text-xs font-semibold inline-flex items-center gap-1.5 transition-all shadow-sm cursor-pointer"
                  >
                    <span>Solve on {p.platform}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>

                  {/* Quick Verdict Logging Buttons */}
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => handleVerdict(p, true)}
                      disabled={isSubmitting}
                      className="flex items-center gap-1 px-2.5 py-1 rounded bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-[11px] font-medium transition-colors cursor-pointer disabled:opacity-50"
                      title="Mark as Accepted (updates BKT mastery & Elo)"
                    >
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                      AC
                    </button>
                    <button
                      onClick={() => handleVerdict(p, false)}
                      disabled={isSubmitting}
                      className="flex items-center gap-1 px-2.5 py-1 rounded bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-[11px] font-medium transition-colors cursor-pointer disabled:opacity-50"
                      title="Mark as Wrong Answer (updates BKT mastery & Elo)"
                    >
                      <XCircle className="w-3.5 h-3.5 text-rose-400" />
                      WA
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
