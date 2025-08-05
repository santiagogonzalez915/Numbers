import React from "react";

function formatTime(seconds) {
  if (seconds == null) return "-";
  const mins = Math.floor(seconds / 60);
  const secs = Math.round(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, "0")}`;
}

export default function StatsModal({ open, onClose, stats, loading, error, refreshStats, isGuest }) {
  if (!open) return null;
  const winRate = stats && stats.games_played > 0 ? ((stats.games_won / stats.games_played) * 100).toFixed(1) : null;
  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-[1000]">
      <div className="bg-white rounded-2xl p-8 min-w-[320px] min-h-[250px] relative shadow-2xl w-full max-w-md">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 bg-gray-100 hover:bg-gray-200 border-none rounded px-3 py-1 text-gray-700 font-semibold text-sm shadow transition"
        >
          Close
        </button>
        <div className="mt-8">
          <h2 className="text-2xl font-bold mb-4 text-indigo-700 flex items-center gap-2">Stats {isGuest && <span className="text-base text-gray-400">(Guest)</span>}</h2>
          <button onClick={refreshStats} className="mb-3 px-3 py-1 rounded bg-indigo-100 hover:bg-indigo-200 text-indigo-800 font-semibold transition">Refresh</button>
          {loading && <div>Loading...</div>}
          {error && <div className="text-red-600 mb-2">{error}</div>}
          {stats ? (
            <ul className="list-none p-0 text-base space-y-1">
              <li>Games Played: {stats.games_played}</li>
              <li>Games Won: {stats.games_won}</li>
              <li>Win Rate: {winRate !== null ? `${winRate}%` : '-'}</li>
              <li>Average Moves: {stats.average_moves}</li>
              <li>Total Moves: {stats.total_moves}</li>
              <li>Best Time: {formatTime(stats.best_time)}</li>
              <li>Average Time: {formatTime(stats.average_time)}</li>
              <li>Current Win Streak: {stats.current_win_streak}</li>
              <li>Longest Win Streak: {stats.longest_win_streak}</li>
            </ul>
          ) : !loading && !error ? (
            <div>No stats available.</div>
          ) : null}
        </div>
      </div>
    </div>
  );
}