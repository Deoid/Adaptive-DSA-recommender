import React, { useState } from 'react';
import { X, Check } from 'lucide-react';
import { authApi } from '../api';

export default function SettingsModal({ user, onClose, onSaveSuccess }) {
  const [cfHandle, setCfHandle] = useState(user?.codeforces_handle || '');
  const [lcHandle, setLcHandle] = useState(user?.leetcode_handle || '');
  const [ccHandle, setCcHandle] = useState(user?.codechef_handle || '');
  const [atHandle, setAtHandle] = useState(user?.atcoder_handle || '');
  const [targetRating, setTargetRating] = useState(user?.target_rating || 1600);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authApi.updateHandles({
        codeforces_handle: cfHandle,
        leetcode_handle: lcHandle,
        codechef_handle: ccHandle,
        atcoder_handle: atHandle,
        target_rating: Number(targetRating),
      });
      onSaveSuccess();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-white">Platform Handles & Target</h2>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs text-slate-400 block mb-1">Codeforces Handle</label>
            <input
              type="text"
              value={cfHandle}
              onChange={(e) => setCfHandle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white"
              placeholder="e.g. tourist"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">LeetCode Username</label>
            <input
              type="text"
              value={lcHandle}
              onChange={(e) => setLcHandle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white"
              placeholder="e.g. neal_wu"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">CodeChef Handle</label>
            <input
              type="text"
              value={ccHandle}
              onChange={(e) => setCcHandle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white"
              placeholder="e.g. gennady"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">AtCoder Username</label>
            <input
              type="text"
              value={atHandle}
              onChange={(e) => setAtHandle(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white"
              placeholder="e.g. tourist"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">Target Elo Rating Goal</label>
            <input
              type="number"
              value={targetRating}
              onChange={(e) => setTargetRating(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-md shadow-indigo-600/25 disabled:opacity-50 cursor-pointer"
          >
            {loading ? 'Saving...' : 'Update & Re-sync'}
          </button>
        </form>
      </div>
    </div>
  );
}
