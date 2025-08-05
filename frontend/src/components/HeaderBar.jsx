import React from "react";
import Timer from "./Timer";
import DifficultySelector from "./DifficultySelector";
import numbersLogo from "../assets/numbers_logo.png";
import statsIcon from "../assets/stats.png";
import signOutIcon from "../assets/sign_out.png";

export default function HeaderBar({ 
  onSignOut, 
  onShowStats, 
  isGuest, 
  user,
  timerKey,
  timerRunning,
  onTimerComplete,
  difficulty,
  onDifficultyChange
}) {
  return (
    <header className="sticky top-0 z-50 bg-slate-800/80 backdrop-blur-md border-b border-blue-500/30">
      <div className="max-w-6xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <img 
              src={numbersLogo} 
              alt="Numbers Game" 
              className="h-8 object-contain"
            />
          </div>
          
          {/* Game Controls */}
          <div className="flex items-center space-x-4">
            {/* Timer */}
            <div className="animate-scale-in">
              <Timer 
                key={timerKey} 
                running={timerRunning} 
                onComplete={onTimerComplete} 
              />
            </div>
            
            {/* Difficulty Selector */}
            <DifficultySelector
              difficulty={difficulty}
              onChange={onDifficultyChange}
            />
            
            {/* Stats Button */}
            <button 
              onClick={onShowStats} 
              className="btn btn-secondary px-3 py-2"
            >
              <img src={statsIcon} alt="Stats" className="h-6 w-auto" />
            </button>
            
            {/* User Menu */}
            <div className="flex items-center space-x-2">
              {isGuest ? (
                <span className="text-sm text-blue-300">👤 Guest</span>
              ) : (
                <span className="text-sm text-blue-300">
                  👤 {user?.username || 'User'}
                </span>
              )}
              <button 
                onClick={onSignOut} 
                className="btn btn-primary px-3 py-2"
              >
                <img src={signOutIcon} alt="Sign Out" className="h-6 w-auto" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
} 