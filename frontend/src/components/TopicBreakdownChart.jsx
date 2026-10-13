import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { PieChart, BarChart3 } from 'lucide-react';

const COLORS = [
  '#6366f1', // Indigo
  '#8b5cf6', // Violet
  '#ec4899', // Pink
  '#f43f5e', // Rose
  '#f97316', // Orange
  '#eab308', // Amber
  '#10b981', // Emerald
  '#06b6d4', // Cyan
  '#3b82f6', // Blue
  '#a855f7', // Purple
];

export default function TopicBreakdownChart({ topicBreakdown }) {
  const data = Object.entries(topicBreakdown || {}).map(([topic, count], idx) => ({
    name: topic,
    shortName: topic.length > 18 ? topic.substring(0, 16) + '..' : topic,
    count: count,
    color: COLORS[idx % COLORS.length],
  }));

  const total = data.reduce((acc, curr) => acc + curr.count, 0);

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-bold text-white">
              Combined Solves Categorized per DSA Topic
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Aggregated across all 4 platforms and unified into canonical computer science domains.
          </p>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 block">Total Tagged AC Solves</span>
          <span className="text-lg font-bold font-mono text-indigo-300">{total}</span>
        </div>
      </div>

      {/* Chart */}
      <div className="h-72 w-full">
        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 45 }}>
              <XAxis
                dataKey="shortName"
                angle={-35}
                textAnchor="end"
                interval={0}
                stroke="#64748b"
                tick={{ fontSize: 11, fill: '#94a3b8' }}
              />
              <YAxis stroke="#64748b" tick={{ fontSize: 11, fill: '#94a3b8' }} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const d = payload[0].payload;
                    return (
                      <div className="bg-slate-950 border border-slate-800 rounded-lg p-2.5 shadow-xl text-xs">
                        <span className="font-semibold text-white block">{d.name}</span>
                        <span className="text-indigo-400 font-mono font-bold">
                          {d.count} solved
                        </span>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="flex items-center justify-center h-full text-slate-500 text-sm">
            No topic data available yet. Click "Sync Platforms" above to populate.
          </div>
        )}
      </div>

      {/* Topic Grid Summary */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 mt-4 pt-4 border-t border-slate-800/80">
        {data.map((item) => (
          <div
            key={item.name}
            className="bg-slate-950/50 border border-slate-800/60 rounded-lg p-2 flex items-center justify-between"
          >
            <div className="truncate mr-2">
              <span className="text-[11px] text-slate-300 truncate block" title={item.name}>
                {item.name}
              </span>
            </div>
            <span
              className="text-xs font-mono font-bold px-1.5 py-0.5 rounded"
              style={{ backgroundColor: `${item.color}20`, color: item.color }}
            >
              {item.count}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
