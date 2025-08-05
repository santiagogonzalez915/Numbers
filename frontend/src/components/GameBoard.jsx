import React from "react";
import TargetDisplay from "./TargetDisplay";
import NumbersGrid from "./NumbersGrid";
import OperationBar from "./OperationBar";
import FeedbackBar from "./FeedbackBar";
import MoveHistory from "./MoveHistory";
import NewGameButton from "./NewGameButton";
import Timer from "./Timer";
import DifficultySelector from "./DifficultySelector";

export default function GameBoard({
  gameState,
  selectedNumber1,
  selectedNumber2,
  selectedOperation,
  feedback,
  onNumberClick,
  onOperationClick,
  onUndo,
  canUndo,
  historyStack,
  onNewGame,
  onShowStats,
  onSignOut,
  isGuest,
  user,
  timerKey,
  timerRunning,
  onTimerComplete,
  onTimerTick,
  difficulty,
  onDifficultyChange,
  numbersLogo
}) {
  return (
    <div className="animate-fade-in-up">
      {/* Game Header */}
      <div className="game-header mb-8">
        {/* Title Row */}
        <div className="title-section flex items-center justify-center mb-6">
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <img 
              src={numbersLogo} 
              alt="Numbers Game" 
              className="h-48 w-auto"
            />
          </div>
        </div>
      </div>

      {/* Main Game Area */}
      <div className="main-game-area flex gap-8">
        {/* Left Side - Move History */}
        <div className="left-sidebar w-80">
          <div className="animate-scale-in" style={{ animationDelay: '0.3s' }}>
            <MoveHistory history={gameState?.steps || []} />
          </div>
        </div>

        {/* Center - Game Content */}
        <div className="flex-1 space-y-8">
          {/* Target Display */}
          <div className="animate-scale-in">
            <TargetDisplay target={gameState?.target} />
          </div>
          
          {/* Numbers Grid */}
          <div className="card animate-scale-in" style={{ animationDelay: '0.1s' }}>
            <NumbersGrid
              numbers={gameState?.numbers || []}
              selectedNumber1={selectedNumber1}
              selectedNumber2={selectedNumber2}
              onNumberClick={onNumberClick}
            />
          </div>
          
          {/* Operation Bar */}
          <div className="card animate-scale-in" style={{ animationDelay: '0.2s' }}>
            <OperationBar
              selectedOperation={selectedOperation}
              onOperationClick={onOperationClick}
              onUndo={onUndo}
              canUndo={canUndo}
            />
          </div>
          
          {/* Feedback */}
          <div className="animate-scale-in" style={{ animationDelay: '0.3s' }}>
            <FeedbackBar message={feedback} />
          </div>
        </div>

        {/* Right Side - Controls */}
        <div className="right-sidebar w-80 space-y-6">
          {/* Timer */}
          <div className="animate-scale-in">
            <Timer 
              key={timerKey} 
              running={timerRunning} 
              onComplete={onTimerComplete}
              onTick={onTimerTick}
            />
          </div>
          
          {/* Difficulty Selector */}
          <div className="card">
            <DifficultySelector
              difficulty={difficulty}
              onChange={onDifficultyChange}
            />
          </div>
          
          {/* New Game Button */}
          <div className="card">
            <button 
              className="btn btn-primary w-full py-4 text-lg font-semibold"
              onClick={onNewGame}
            >
              New Game
            </button>
          </div>
          
          {/* Stats Button */}
          <div className="card">
            <button 
              onClick={onShowStats} 
              className="btn btn-primary w-full py-4 text-lg font-semibold"
            >
              Stats
            </button>
          </div>
          
          {/* Sign Out Button */}
          <div className="card">
            <button 
              onClick={onSignOut} 
              className="btn btn-primary w-full py-4 text-lg font-semibold"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 