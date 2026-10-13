import React from 'react';
import { Brain, Sparkles, Activity, ShieldAlert, Award } from 'lucide-react';

export default function BktMasteryMatrix({ topics, onSelectTopicForPractice }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Mastered':
        return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'Competent':
        return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      case 'Developing':
        return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      default:
        return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
    }
  };

  const getProgressBarColor = (prob) => {
    if (prob >= 0.8) return 'from-emerald-500 to-teal-400';
    if (prob >= 0.6) return 'from-blue-500 to-indigo-400';
    if (prob >= 0.35) return 'from-amber-500 to-yellow-400';
    return 'from-rose-500 to-pink-500';
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-bold text-white">
              Bayesian Knowledge Tracing (BKT) Mastery Vector
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Calculated over a sliding window of the last 20 submissions per topic. Updates after every Accepted / Wrong-Answer verdict.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">Novice (&lt;35%)</span>
          <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">Dev (35-59%)</span>
          <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">Comp (60-79%)</span>
          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Master (80%+)</span>
        </div>
      </div>

      {/* Grid of Topics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
        {(topics || []).map((t) => {
          const prob = t.mastery_probability;
          const pct = Math.round(prob * 100);

          return (
            <div
              key={t.topic}
              className="bg-slate-950/70 border border-slate-800/80 hover:border-slate-700 rounded-xl p-4 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="text-sm font-semibold text-white truncate" title={t.topic}>
                    {t.topic}
                  </h3>
                  <span
                    className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${getStatusColor(
                      t.status
                    )}`}
                  >
                    {t.status}
                  </span>
                </div>

                {/* Probability Bar */}
                <div className="space-y-1 mb-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-400 font-mono text-[11px]">P(Mastery)</span>
                    <span className="font-mono font-bold text-white">{pct}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-full rounded-full bg-gradient-to-r ${getProgressBarColor(prob)} transition-all duration-500`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Stats Footer */}
              <div className="pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
                <div className="flex items-center gap-1 font-mono">
                  <Award className="w-3.5 h-3.5 text-amber-400" />
                  <span>Elo: {Math.round(t.topic_elo)}</span>
                </div>
                <div className="flex items-center gap-1">
                  <span>Window: {Math.round((t.recent_accuracy || 0) * 100)}% AC</span>
                </div>
                {onSelectTopicForPractice && (
                  <button
                    onClick={() => onSelectTopicForPractice(t.topic)}
                    className="px-2 py-0.5 rounded bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 hover:text-white border border-indigo-500/40 text-[11px] font-medium transition-all flex items-center gap-1 cursor-pointer"
                    title={`Surfaces recommended ${t.topic} problems`}
                  >
                    <span>Train</span>
                    <span>&darr;</span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
