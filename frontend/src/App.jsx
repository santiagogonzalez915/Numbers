import React, { useState, useEffect } from "react";
import AuthPanel from "./components/AuthPanel";
import GameBoard from "./components/GameBoard";
import StatsModal from "./components/StatsModal";
import WinModal from "./components/WinModal";
import Timer from "./components/Timer";
import DifficultySelector from "./components/DifficultySelector";
import useGame from "./hooks/useGame";
import useAuth from "./hooks/useAuth";
import useStats from "./hooks/useStats";
import numbersLogo from "./assets/numbers_logo.png";

export default function App() {
  const auth = useAuth();
  const [statsOpen, setStatsOpen] = useState(false);
  const [winModalOpen, setWinModalOpen] = useState(false);
  const game = useGame(auth.token);
  const stats = useStats(auth.token);

  useEffect(() => {
    stats.refreshStats();
  }, [game.timerKey]); 

  useEffect(() => {
    if (game.gameState && game.gameState.completed) {
      stats.refreshStats();
      setWinModalOpen(true);
    }
  }, [game.gameState && game.gameState.completed]);

  if (!auth.token) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100">
        <div className="w-full max-w-md bg-white/90 backdrop-blur-md rounded-2xl shadow-xl p-8 flex flex-col gap-6 border border-slate-200">
          <AuthPanel onAuth={auth.setToken} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-slate-100 via-slate-50 to-slate-100">
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-4xl mx-auto">
          <StatsModal 
            open={statsOpen} 
            onClose={() => setStatsOpen(false)} 
            stats={stats.stats} 
            loading={stats.loading} 
            error={stats.error} 
            refreshStats={stats.refreshStats} 
            isGuest={auth.isGuest} 
          />
          <WinModal
            open={winModalOpen}
            onClose={() => setWinModalOpen(false)}
            onNewGame={game.handleNewGame}
            onShowStats={() => setStatsOpen(true)}
            elapsedTime={game.elapsedTime}
            difficulty={game.difficulty}
          />
          <GameBoard
            gameState={game.gameState}
            selectedNumber1={game.selectedNumber1}
            selectedNumber2={game.selectedNumber2}
            selectedOperation={game.selectedOperation}
            feedback={game.feedback}
            onNumberClick={game.handleNumberClick}
            onOperationClick={game.handleOperationClick}
            onUndo={game.handleUndo}
            canUndo={game.historyStack.length > 0}
            historyStack={game.historyStack}
            onNewGame={game.handleNewGame}
            onShowStats={() => setStatsOpen(true)}
            onSignOut={auth.logout}
            isGuest={auth.isGuest}
            user={auth.user}
            timerKey={game.timerKey}
            timerRunning={game.timerRunning}
            onTimerComplete={game.setElapsedTime}
            onTimerTick={game.handleTimerTick}
            difficulty={game.difficulty}
            onDifficultyChange={game.handleDifficultyChange}
            numbersLogo={numbersLogo}
          />
        </div>
      </div>
    </div>
  );
}
