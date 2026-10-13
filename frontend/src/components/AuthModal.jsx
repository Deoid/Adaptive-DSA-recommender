import React, { useState } from 'react';
import { Layers, ShieldCheck, UserCheck, AlertCircle } from 'lucide-react';
import { authApi } from '../api';

export default function AuthModal({ onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('tourist_coder');
  const [email, setEmail] = useState('tourist@example.com');
  const [password, setPassword] = useState('Password123!');
  const [cfHandle, setCfHandle] = useState('tourist');
  const [lcHandle, setLcHandle] = useState('neal_wu');
  const [ccHandle, setCcHandle] = useState('gennady');
  const [atHandle, setAtHandle] = useState('tourist');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let res;
      if (isRegister) {
        res = await authApi.register({
          username,
          email,
          password,
          codeforces_handle: cfHandle,
          leetcode_handle: lcHandle,
          codechef_handle: ccHandle,
          atcoder_handle: atHandle,
        });
      } else {
        res = await authApi.login(username, password);
      }

      const token = res.data.access_token;
      localStorage.setItem('dsa_token', token);
      onLoginSuccess(res.data.user);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail || 'Authentication failed. Please check your credentials.'
      );
    } finally {
      setLoading(false);
    }
  };

  const loadDemoUser = () => {
    setUsername('tourist_coder');
    setPassword('Password123!');
    setIsRegister(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mx-auto mb-3 shadow-lg shadow-indigo-500/25">
            <Layers className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-xl font-bold text-white">
            {isRegister ? 'Create Coder Profile' : 'Sign In to Adaptive DSA'}
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Bayesian Knowledge Tracing & Multi-Platform Skill Tracking
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">
              Username or Email
            </label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="e.g. tourist_coder"
            />
          </div>

          {isRegister && (
            <div>
              <label className="text-xs font-medium text-slate-400 block mb-1">
                Email Address
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                placeholder="name@example.com"
              />
            </div>
          )}

          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
              placeholder="••••••••"
            />
          </div>

          {isRegister && (
            <div className="pt-2 border-t border-slate-800 space-y-2.5">
              <span className="text-xs font-semibold text-indigo-400 block">
                Link Platform Handles:
              </span>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] text-slate-400 block">Codeforces</label>
                  <input
                    type="text"
                    value={cfHandle}
                    onChange={(e) => setCfHandle(e.target.value)}
                    placeholder="tourist"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-400 block">LeetCode</label>
                  <input
                    type="text"
                    value={lcHandle}
                    onChange={(e) => setLcHandle(e.target.value)}
                    placeholder="neal_wu"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-400 block">CodeChef</label>
                  <input
                    type="text"
                    value={ccHandle}
                    onChange={(e) => setCcHandle(e.target.value)}
                    placeholder="gennady"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-[11px] text-slate-400 block">AtCoder</label>
                  <input
                    type="text"
                    value={atHandle}
                    onChange={(e) => setAtHandle(e.target.value)}
                    placeholder="tourist"
                    className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-white"
                  />
                </div>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-md shadow-indigo-600/25 disabled:opacity-50 cursor-pointer mt-4"
          >
            {loading ? 'Processing...' : isRegister ? 'Register & Connect' : 'Sign In'}
          </button>
        </form>

        <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <button
            onClick={() => setIsRegister(!isRegister)}
            className="hover:text-white transition-colors cursor-pointer"
          >
            {isRegister ? 'Already have an account? Sign In' : 'Need an account? Register'}
          </button>

          {!isRegister && (
            <button
              onClick={loadDemoUser}
              className="text-indigo-400 hover:text-indigo-300 font-medium cursor-pointer"
            >
              Fill Demo User
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
