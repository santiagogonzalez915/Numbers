import { useState, useEffect, useCallback } from "react";
import api from "../api/axios.js";

export default function useStats(token) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isGuest = token === "guest";

  const fetchStats = useCallback(async () => {
    if (isGuest) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get("/user/stats");
      setStats(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch stats");
    } finally {
      setLoading(false);
    }
  }, [isGuest]);

  useEffect(() => {
    if (!isGuest && token) {
      fetchStats();
    } else if (isGuest) {
      setStats({ games_played: 0, games_won: 0, average_moves: 0, best_time: null });
    }
  }, [token, isGuest, fetchStats]);

  const updateGuestStats = (updater) => {
    if (!isGuest) return;
    setStats((prev) => ({ ...prev, ...updater(prev) }));
  };

  return {
    stats,
    loading,
    error,
    refreshStats: fetchStats,
    updateGuestStats,
  };
} 