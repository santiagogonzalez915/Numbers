import React, { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function AuthPanel({ onAuth }) {
  const [showRegister, setShowRegister] = useState(false);

  const handleGuest = () => {
    localStorage.setItem("token", "guest");
    if (onAuth) onAuth("guest");
  };

  return (
    <div className="flex flex-col items-center gap-4 w-full">
      {showRegister ? (
        <>
          <RegisterForm onRegister={() => setShowRegister(false)} />
          <div>
            Already have an account? <button className="text-indigo-600 hover:underline" onClick={() => setShowRegister(false)}>Log in</button>
          </div>
          <div className="mt-2">
            <button className="px-4 py-2 rounded bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold transition" onClick={handleGuest}>Play as Guest</button>
          </div>
        </>
      ) : (
        <>
          <LoginForm onLogin={onAuth} />
          <div>
            Don't have an account? <button className="text-indigo-600 hover:underline" onClick={() => setShowRegister(true)}>Register</button>
          </div>
          <div className="mt-2">
            <button className="px-4 py-2 rounded bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold transition" onClick={handleGuest}>Play as Guest</button>
          </div>
        </>
      )}
    </div>
  );
} 