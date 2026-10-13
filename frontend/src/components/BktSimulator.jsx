import React, { useState } from 'react';
import { Play, RotateCcw, LineChart, Cpu } from 'lucide-react';
import { bktApi } from '../api';

export default function BktSimulator() {
  const [prior, setPrior] = useState(0.15);
  const [userElo, setUserElo] = useState(1300);
  const [problemDiff, setProblemDiff] = useState(1450);
  const [verdicts, setVerdicts] = useState([true, true, false, true, true]);
  const [simResult, setSimResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const addVerdict = (v) => {
    if (verdicts.length < 15) {
      setVerdicts([...verdicts, v]);
    }
  };

  const clearVerdicts = () => {
    setVerdicts([]);
    setSimResult(null);
  };

  const handleSimulate = async () => {
    if (verdicts.length === 0) return;
    setLoading(true);
    try {
      const res = await bktApi.simulate({
        initial_p_l: Number(prior),
        verdicts: verdicts,
        user_elo: Number(userElo),
        problem_difficulty: Number(problemDiff),
      });
      setSimResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-pink-400" />
          <h2 className="text-lg font-bold text-white">
            Interactive BKT & Elo Algorithm Sandbox
          </h2>
        </div>
        <span className="text-xs text-slate-400">
          Simulate Bayesian posterior updates across hypothetical submissions
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Prior & Elo Inputs */}
        <div className="space-y-3 bg-slate-950/70 p-4 rounded-xl border border-slate-800/80">
          <div>
            <label className="text-xs text-slate-400 block mb-1">
              Initial Prior P(L₀): <strong className="text-white font-mono">{prior}</strong>
            </label>
            <input
              type="range"
              min="0.05"
              max="0.80"
              step="0.05"
              value={prior}
              onChange={(e) => setPrior(parseFloat(e.target.value))}
              className="w-full accent-indigo-500 cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">
              Baseline Solver Elo: <strong className="text-white font-mono">{userElo}</strong>
            </label>
            <input
              type="number"
              value={userElo}
              onChange={(e) => setUserElo(parseInt(e.target.value) || 1200)}
              className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-white font-mono"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">
              Problem Elo Rating: <strong className="text-white font-mono">{problemDiff}</strong>
            </label>
            <input
              type="number"
              value={problemDiff}
              onChange={(e) => setProblemDiff(parseInt(e.target.value) || 1400)}
              className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-white font-mono"
            />
          </div>
        </div>

        {/* Verdict Sequence Builder */}
        <div className="md:col-span-2 space-y-3 bg-slate-950/70 p-4 rounded-xl border border-slate-800/80 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300">
                Attempt Sequence ({verdicts.length} steps):
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => addVerdict(true)}
                  className="px-2.5 py-1 rounded bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold hover:bg-emerald-600/40 cursor-pointer"
                >
                  + Add AC
                </button>
                <button
                  onClick={() => addVerdict(false)}
                  className="px-2.5 py-1 rounded bg-rose-600/30 text-rose-300 border border-rose-500/40 text-xs font-semibold hover:bg-rose-600/40 cursor-pointer"
                >
                  + Add WA
                </button>
                <button
                  onClick={clearVerdicts}
                  className="p-1 rounded text-slate-400 hover:text-slate-200 cursor-pointer"
                  title="Reset Sequence"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Sequence Pills */}
            <div className="flex flex-wrap gap-1.5 min-h-[42px] p-2 bg-slate-900/80 rounded-lg border border-slate-800/70">
              {verdicts.map((v, i) => (
                <span
                  key={i}
                  className={`text-xs font-mono font-bold px-2.5 py-1 rounded-md border ${
                    v
                      ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30'
                      : 'bg-rose-500/10 text-rose-300 border-rose-500/30'
                  }`}
                >
                  #{i + 1} {v ? 'AC' : 'WA'}
                </span>
              ))}
              {verdicts.length === 0 && (
                <span className="text-xs text-slate-500">
                  Click "+ Add AC" or "+ Add WA" to build an attempt sequence...
                </span>
              )}
            </div>
          </div>

          <button
            onClick={handleSimulate}
            disabled={loading || verdicts.length === 0}
            className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-gradient-to-r from-pink-600 to-indigo-600 hover:from-pink-500 hover:to-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/20 disabled:opacity-50 cursor-pointer"
          >
            <Play className="w-3.5 h-3.5" />
            {loading ? 'Computing Posterior...' : 'Run Bayesian Simulation'}
          </button>
        </div>
      </div>

      {/* Results View */}
      {simResult && (
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/90 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <span className="text-xs text-slate-400 block">Final BKT Mastery</span>
            <span className="text-3xl font-black font-mono text-emerald-400">
              {Math.round(simResult.bkt_result.mastery_probability * 100)}%
            </span>
            <span className="text-xs text-slate-400 block mt-1">
              Status: <strong className="text-white">{simResult.bkt_result.status}</strong>
            </span>
          </div>

          <div>
            <span className="text-xs text-slate-400 block">Simulated Elo Shift</span>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-black font-mono text-amber-400">
                {Math.round(simResult.final_elo)}
              </span>
              <span className="text-xs font-mono text-slate-400">
                (Δ {Math.round(simResult.final_elo - userElo)})
              </span>
            </div>
            <span className="text-xs text-slate-400 block mt-1">
              Zone: <strong className="text-white">{simResult.zpd_evaluation.difficulty_tier}</strong>
            </span>
          </div>

          <div>
            <span className="text-xs text-slate-400 block">Stepwise P(L) Trajectory</span>
            <div className="flex items-center gap-1 font-mono text-xs text-slate-300 mt-2 flex-wrap">
              {simResult.bkt_result.history.map((h, idx) => (
                <span
                  key={idx}
                  className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-[11px]"
                >
                  {Math.round(h * 100)}%
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
