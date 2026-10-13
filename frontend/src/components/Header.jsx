import React, { useState } from 'react';
import { RefreshCw, User, LogOut, Settings, Award, Layers } from 'lucide-react';

export default function Header({ user, onLogout, onSync, syncing, onOpenSettings }) {
  return (
    <header className="bg-slate-900/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Layers className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                Adaptive DSA Recommender
              </h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 font-mono">
                BKT + Elo Engine
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Cross-Platform (CF · LC · CC · AC) Skill Growth Optimizer
            </p>
          </div>
        </div>

        {/* User Controls & Unified Skill */}
        <div className="flex items-center gap-3">
          {user && (
            <>
              {/* Unified Elo Badge */}
              <div className="flex items-center gap-2 bg-slate-800/80 border border-slate-700/60 rounded-lg px-3 py-1.5 shadow-inner">
                <Award className="w-4 h-4 text-amber-400" />
                <div className="text-left">
                  <span className="text-[10px] text-slate-400 uppercase tracking-wider block leading-none">
                    Unified Elo
                  </span>
                  <span className="text-sm font-bold font-mono text-amber-300">
                    {user.overall_elo || 1300}
                  </span>
                </div>
              </div>

              {/* Sync Button */}
              <button
                onClick={onSync}
                disabled={syncing}
                className="flex items-center gap-2 px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 transition-all disabled:opacity-50 cursor-pointer"
                title="Sync submissions and recalculate Bayesian mastery"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin' : ''}`} />
                {syncing ? 'Syncing...' : 'Sync Platforms'}
              </button>

              {/* Settings / Handles button */}
              <button
                onClick={onOpenSettings}
                className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition-colors cursor-pointer"
                title="Manage Connected Handles"
              >
                <Settings className="w-4 h-4" />
              </button>

              {/* Logout button */}
              <button
                onClick={onLogout}
                className="p-2 rounded-lg bg-slate-800 hover:bg-red-950/60 hover:text-red-400 text-slate-400 border border-slate-700 transition-colors cursor-pointer"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
