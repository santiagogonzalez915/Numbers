import React from "react";

export default function WinModal({ open, onClose, onNewGame, onShowStats, elapsedTime, difficulty }) {
  if (!open) return null;

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getDifficultyName = (level) => {
    switch (level) {
      case 1: return "Easy";
      case 2: return "Medium";
      case 3: return "Hard";
      default: return "Easy";
    }
  };

  const handleNewGame = () => {
    onNewGame();
    onClose();
  };

  const handleViewStats = () => {
    onShowStats();
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 animate-slide-in-up">
        {/* Success Icon */}
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>

        {/* Title */}
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-2">
          🎉 Congratulations! 🎉
        </h2>
        
        <p className="text-center text-gray-600 mb-6">
          You've completed the puzzle!
        </p>

        {/* Game Stats */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <p className="text-sm text-gray-500 font-medium">Time</p>
              <p className="text-lg font-bold text-gray-900">{formatTime(elapsedTime)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Difficulty</p>
              <p className="text-lg font-bold text-gray-900">{getDifficultyName(difficulty)}</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col gap-3">
          <button
            onClick={handleNewGame}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200"
          >
            Play Again
          </button>
          
          <button
            onClick={handleViewStats}
            className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors duration-200"
          >
            View Statistics
          </button>
          
          <button
            onClick={onClose}
            className="w-full bg-transparent hover:bg-gray-50 text-gray-500 font-medium py-2 px-4 rounded-lg transition-colors duration-200"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
} 