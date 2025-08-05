import React, { useState } from "react";
import axios from "axios";

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const params = new URLSearchParams();
      params.append("username", username);
      params.append("password", password);
      const response = await axios.post(
        "/user/login",
        params,
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );
      const { access_token } = response.data;
      localStorage.setItem("token", access_token);
      if (onLogin) onLogin(access_token);
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-xs mx-auto flex flex-col gap-4 p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-2xl font-bold mb-2 text-indigo-700">Login</h2>
      <input
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
        required
        className="px-3 py-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        required
        className="px-3 py-2 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-200"
      />
      <button type="submit" className="mt-2 px-4 py-2 rounded bg-indigo-500 hover:bg-indigo-600 text-white font-semibold transition">Login</button>
      {error && <div className="text-red-600 text-sm mt-1">{error}</div>}
    </form>
  );
} 