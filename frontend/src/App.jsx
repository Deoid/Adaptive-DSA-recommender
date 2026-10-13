import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import PlatformCards from './components/PlatformCards';
import TopicBreakdownChart from './components/TopicBreakdownChart';
import BktMasteryMatrix from './components/BktMasteryMatrix';
import RecommendationFeed from './components/RecommendationFeed';
import BktSimulator from './components/BktSimulator';
import AuthModal from './components/AuthModal';
import SettingsModal from './components/SettingsModal';
import { authApi, platformApi, bktApi, recApi } from './api';

export default function App() {
  const [user, setUser] = useState(null);
  const [authChecked, setAuthChecked] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Core Data States
  const [platformStats, setPlatformStats] = useState(null);
  const [bktTopics, setBktTopics] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [recsLoading, setRecsLoading] = useState(false);

  // Recommendation Filter States
  const [mode, setMode] = useState('balanced');
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [showInspector, setShowInspector] = useState(false);

  // Check existing token on mount
  useEffect(() => {
    const token = localStorage.getItem('dsa_token');
    if (token) {
      authApi
        .getMe()
        .then((res) => {
          setUser(res.data);
          loadAllData();
        })
        .catch(() => {
          localStorage.removeItem('dsa_token');
          setUser(null);
        })
        .finally(() => setAuthChecked(true));
    } else {
      setAuthChecked(true);
    }
  }, []);

  // Reload recommendations whenever filter changes
  useEffect(() => {
    if (user) {
      loadRecommendations();
    }
  }, [mode, selectedTopic, selectedPlatform]);

  const loadAllData = async () => {
    try {
      const [statsRes, masteryRes] = await Promise.all([
        platformApi.getStats(),
        bktApi.getMastery(),
      ]);
      setPlatformStats(statsRes.data);
      setBktTopics(masteryRes.data.topics || []);
      await loadRecommendations();
    } catch (err) {
      console.error('Error loading dashboard metrics:', err);
    }
  };

  const loadRecommendations = async () => {
    setRecsLoading(true);
    try {
      const params = { mode };
      if (selectedTopic) params.topic = selectedTopic;
      if (selectedPlatform) params.platform = selectedPlatform;
      params.limit = 12;

      const res = await recApi.getRecommendations(params);
      setRecommendations(res.data.recommendations || []);
    } catch (err) {
      console.error('Error loading recommendations:', err);
    } finally {
      setRecsLoading(false);
    }
  };

  const handleSync = async () => {
    setSyncing(true);
    try {
      const res = await platformApi.sync();
      setPlatformStats(res.data.data);
      // Reload BKT mastery and recommendations after sync
      const masteryRes = await bktApi.getMastery();
      setBktTopics(masteryRes.data.topics || []);
      await loadRecommendations();
    } catch (err) {
      console.error('Failed to sync platforms:', err);
    } finally {
      setSyncing(false);
    }
  };

  const handleSubmitVerdict = async (payload) => {
    try {
      await bktApi.submitVerdict(payload);
      // Refresh user, BKT vector, and recommendation feed immediately!
      const [userRes, masteryRes] = await Promise.all([
        authApi.getMe(),
        bktApi.getMastery(),
      ]);
      setUser(userRes.data);
      setBktTopics(masteryRes.data.topics || []);
      await loadRecommendations();
    } catch (err) {
      console.error('Error submitting verdict:', err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('dsa_token');
    setUser(null);
    setPlatformStats(null);
    setBktTopics([]);
    setRecommendations([]);
  };

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    loadAllData();
  };

  if (!authChecked) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-400">
        Initializing Adaptive Recommendation Engine...
      </div>
    );
  }

  const topicsList = bktTopics.map((t) => t.topic);

  const handleSelectTopicForPractice = (topic) => {
    setSelectedTopic(topic);
    setTimeout(() => {
      const el = document.getElementById('recommendations-section');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 50);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-indigo-500/30">
      {!user && <AuthModal onLoginSuccess={handleLoginSuccess} />}

      {settingsOpen && user && (
        <SettingsModal
          user={user}
          onClose={() => setSettingsOpen(false)}
          onSaveSuccess={() => {
            authApi.getMe().then((res) => setUser(res.data));
            handleSync();
          }}
        />
      )}

      <Header
        user={user}
        onLogout={handleLogout}
        onSync={handleSync}
        syncing={syncing}
        onOpenSettings={() => setSettingsOpen(true)}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
        {/* Platform Ratings and Total Solved Problem Counters */}
        <PlatformCards
          ratings={platformStats?.ratings}
          solvedStats={platformStats?.problems_solved}
        />

        {/* 2-Column Grid: Solved Breakdown Chart + BKT Mastery Matrix */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          <TopicBreakdownChart
            topicBreakdown={platformStats?.problems_solved?.topic_breakdown}
          />
          <BktMasteryMatrix
            topics={bktTopics}
            onSelectTopicForPractice={handleSelectTopicForPractice}
          />
        </div>

        {/* Adaptive Problem Recommendations (The Core Engine) */}
        <RecommendationFeed
          recommendations={recommendations}
          loading={recsLoading}
          mode={mode}
          setMode={setMode}
          selectedTopic={selectedTopic}
          setSelectedTopic={setSelectedTopic}
          selectedPlatform={selectedPlatform}
          setSelectedPlatform={setSelectedPlatform}
          topicsList={topicsList}
          onSubmitVerdict={handleSubmitVerdict}
        />

        {/* Optional Collapsible Developer / Evaluator Algorithm Inspector */}
        {showInspector && (
          <div className="pt-4 border-t border-slate-800/80">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400">
                Underlying Algorithm Inspector (Dev / Test Mode)
              </span>
              <button
                onClick={() => setShowInspector(false)}
                className="text-xs text-slate-500 hover:text-slate-300 cursor-pointer"
              >
                Hide Inspector &times;
              </button>
            </div>
            <BktSimulator />
          </div>
        )}
      </main>

      {/* Footer with subtle developer inspector toggle */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 px-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500 max-w-7xl mx-auto w-full">
        <span>
          Adaptive DSA Recommendation Engine · Bayesian Knowledge Tracing (BKT) · Elo Rating Systems
        </span>
        <button
          onClick={() => setShowInspector(!showInspector)}
          className="text-slate-500 hover:text-indigo-400 text-[11px] font-mono transition-colors cursor-pointer"
        >
          {showInspector ? 'Hide Algorithm Sandbox' : '🔬 Algorithm Math Inspector'}
        </button>
      </footer>
    </div>
  );
}
