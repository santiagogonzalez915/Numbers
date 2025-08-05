import { useState, useCallback } from "react";
import api from "../api/axios.js";

export default function useAuth() {
  const [token, setTokenState] = useState(() => localStorage.getItem("token"));

  const setToken = useCallback((newToken) => {
    if (newToken) {
      localStorage.setItem("token", newToken);
    } else {
      localStorage.removeItem("token");
    }
    setTokenState(newToken);
  }, []);

  const login = useCallback((token) => {
    setToken(token);
  }, [setToken]);

  const logout = useCallback(() => {
    setToken(null);
  }, [setToken]);

  const isGuest = token === "guest";
  const user = isGuest ? { username: "Guest" } : null;

  return {
    token,
    isGuest,
    user,
    login,
    logout,
    setToken,
  };
} 