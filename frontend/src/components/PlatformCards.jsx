import React from 'react';
import { ExternalLink, CheckCircle2, TrendingUp, Award, Zap } from 'lucide-react';

export default function PlatformCards({ ratings, solvedStats }) {
  const cf = ratings?.codeforces || {};
  const lc = ratings?.leetcode || {};
  const cc = ratings?.codechef || {};
  const at = ratings?.atcoder || {};

  const totalCombined = solvedStats?.combined_total || 0;
  const platformBreakdown = solvedStats?.platform_breakdown || {};

  return (
    <div className="space-y-6">
      {/* Hero: Combined Solved Problems & Skill Level */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 relative overflow-hidden shadow-xl">
        <div className="absolute right-0 top-0 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6 relative z-10">
          <div>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium mb-3">
              <Zap className="w-3.5 h-3.5" /> Multi-Platform Combined Aggregation
            </span>
            <div className="flex items-baseline gap-3">
              <span className="text-5xl font-black font-mono tracking-tight text-white">
                {totalCombined}
              </span>
              <span className="text-slate-400 font-medium text-lg">
                Problems Solved Across 4 Platforms
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-2 max-w-2xl">
              Cross-referenced from Codeforces, LeetCode, CodeChef, and AtCoder. All tagged problems are unified into canonical DSA concepts to drive the Bayesian Knowledge Tracing model.
            </p>
          </div>

          {/* Quick Platform Solved Counter Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 w-full lg:w-auto">
            <div className="bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="text-[11px] text-blue-400 font-medium block">Codeforces</span>
              <span className="text-xl font-bold font-mono text-white">
                {platformBreakdown.codeforces || 0}
              </span>
              <span className="text-[10px] text-slate-500 block">AC Solves</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="text-[11px] text-amber-400 font-medium block">LeetCode</span>
              <span className="text-xl font-bold font-mono text-white">
                {platformBreakdown.leetcode || 0}
              </span>
              <span className="text-[10px] text-slate-500 block">AC Solves</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="text-[11px] text-yellow-500 font-medium block">CodeChef</span>
              <span className="text-xl font-bold font-mono text-white">
                {platformBreakdown.codechef || 0}
              </span>
              <span className="text-[10px] text-slate-500 block">AC Solves</span>
            </div>
            <div className="bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-center">
              <span className="text-[11px] text-emerald-400 font-medium block">AtCoder</span>
              <span className="text-xl font-bold font-mono text-white">
                {platformBreakdown.atcoder || 0}
              </span>
              <span className="text-[10px] text-slate-500 block">AC Solves</span>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Connected Platforms Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Codeforces Card */}
        <div className="bg-slate-900/90 border border-slate-800/80 rounded-xl p-5 hover:border-blue-500/40 transition-all shadow-md group">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center font-bold text-blue-400 text-sm">
                CF
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">Codeforces</h3>
                <span className="text-xs text-slate-400 font-mono">
                  {cf.handle ? `@${cf.handle}` : 'Not Linked'}
                </span>
              </div>
            </div>
            {cf.handle && (
              <a
                href={`https://codeforces.com/profile/${cf.handle}`}
                target="_blank"
                rel="noreferrer"
                className="text-slate-500 hover:text-blue-400 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-end justify-between">
            <div>
              <span className="text-[11px] text-slate-400 block">Official Rating</span>
              <span className="text-2xl font-bold font-mono text-blue-400">
                {cf.rating || 1200}
              </span>
            </div>
            <div className="text-right">
              <span className="text-[11px] text-slate-400 block">Rank</span>
              <span className="text-xs font-medium px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 capitalize">
                {cf.rank || 'Unrated'}
              </span>
            </div>
          </div>
        </div>

        {/* LeetCode Card */}
        <div className="bg-slate-900/90 border border-slate-800/80 rounded-xl p-5 hover:border-amber-500/40 transition-all shadow-md group">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center font-bold text-amber-400 text-sm">
                LC
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">LeetCode</h3>
                <span className="text-xs text-slate-400 font-mono">
                  {lc.handle ? `@${lc.handle}` : 'Not Linked'}
                </span>
              </div>
            </div>
            {lc.handle && (
              <a
                href={`https://leetcode.com/${lc.handle}`}
                target="_blank"
                rel="noreferrer"
                className="text-slate-500 hover:text-amber-400 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-end justify-between">
            <div>
              <span className="text-[11px] text-slate-400 block">Contest Rating</span>
              <span className="text-2xl font-bold font-mono text-amber-400">
                {lc.rating || 1500}
              </span>
            </div>
            <div className="text-right">
              <span className="text-[11px] text-slate-400 block">E / M / H</span>
              <span className="text-xs font-mono text-slate-300">
                {lc.easy || 0} / {lc.medium || 0} / {lc.hard || 0}
              </span>
            </div>
          </div>
        </div>

        {/* CodeChef Card */}
        <div className="bg-slate-900/90 border border-slate-800/80 rounded-xl p-5 hover:border-yellow-500/40 transition-all shadow-md group">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center font-bold text-yellow-400 text-sm">
                CC
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">CodeChef</h3>
                <span className="text-xs text-slate-400 font-mono">
                  {cc.handle ? `@${cc.handle}` : 'Not Linked'}
                </span>
              </div>
            </div>
            {cc.handle && (
              <a
                href={`https://www.codechef.com/users/${cc.handle}`}
                target="_blank"
                rel="noreferrer"
                className="text-slate-500 hover:text-yellow-400 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-end justify-between">
            <div>
              <span className="text-[11px] text-slate-400 block">Rating</span>
              <span className="text-2xl font-bold font-mono text-yellow-400">
                {cc.rating || 1400}
              </span>
            </div>
            <div className="text-right">
              <span className="text-[11px] text-slate-400 block">Stars Tier</span>
              <span className="text-xs font-bold text-yellow-300 px-2 py-0.5 rounded bg-yellow-500/10">
                {cc.stars || '1★'}
              </span>
            </div>
          </div>
        </div>

        {/* AtCoder Card */}
        <div className="bg-slate-900/90 border border-slate-800/80 rounded-xl p-5 hover:border-emerald-500/40 transition-all shadow-md group">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center font-bold text-emerald-400 text-sm">
                AC
              </div>
              <div>
                <h3 className="font-semibold text-white text-sm">AtCoder</h3>
                <span className="text-xs text-slate-400 font-mono">
                  {at.handle ? `@${at.handle}` : 'Not Linked'}
                </span>
              </div>
            </div>
            {at.handle && (
              <a
                href={`https://atcoder.jp/users/${at.handle}`}
                target="_blank"
                rel="noreferrer"
                className="text-slate-500 hover:text-emerald-400 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-end justify-between">
            <div>
              <span className="text-[11px] text-slate-400 block">Algorithm Rating</span>
              <span className="text-2xl font-bold font-mono text-emerald-400">
                {at.rating || 1000}
              </span>
            </div>
            <div className="text-right">
              <span className="text-[11px] text-slate-400 block">Color Tier</span>
              <span className="text-xs font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300">
                {at.tier || 'Gray'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
