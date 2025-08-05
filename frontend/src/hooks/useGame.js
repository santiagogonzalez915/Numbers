import { useState, useEffect, useCallback } from "react";
import axios from "axios";

export default function useGame(token) {
  const [gameState, setGameState] = useState(null);
  const [selectedNumber1, setSelectedNumber1] = useState(null);
  const [selectedNumber2, setSelectedNumber2] = useState(null);
  const [selectedOperation, setSelectedOperation] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [difficulty, setDifficulty] = useState(1);
  const [historyStack, setHistoryStack] = useState([]);
  const [gameId, setGameId] = useState(null);
  const [timerRunning, setTimerRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [timerKey, setTimerKey] = useState(0);

  const handleTimerTick = useCallback((seconds) => {
    setElapsedTime(seconds);
  }, []);

  const getNewGame = useCallback(async (difficulty = 1) => {
    const response = await axios.post("/game/start", { difficulty });
    return response.data;
  }, []);

  useEffect(() => {
    getNewGame(difficulty).then((response) => {
      setGameId(response.game_id);
      setGameState(response);
      setTimerRunning(true);
      setElapsedTime(0);
      setTimerKey((k) => k + 1);
    });
  }, [difficulty]);

  useEffect(() => {
    if (gameState && gameState.completed) {
      setTimerRunning(false);
    }
  }, [gameState]);

  const makeMove = useCallback(async (num1, num2, operation) => {
    const headers = {};
    if (token && token !== "guest") {
      headers["Authorization"] = `Bearer ${token}`;
    }
    
    const opMap = {
      '×': '*',
      '÷': '/',
      '−': '-'
    };
    const convertedOperation = opMap[operation] || operation;
    
    const response = await axios.post(`/game/${gameId}/move`, {
      num1,
      num2,
      operation: convertedOperation,
    }, { headers });
    return response.data;
  }, [gameId, token]);

  const handleNumberClick = async (number) => {
    if (selectedNumber1 === null) {
      setSelectedNumber1(number);
      setFeedback(`Selected ${number}. Now click an operation.`);
      return;
    }
    if (selectedOperation === null) {
      if (selectedNumber1 === number) {
        setSelectedNumber1(null);
        setFeedback("Click a number, then an operation, then another number");
      }
      return;
    }
    if (selectedNumber2 === null && number !== selectedNumber1) {
      setSelectedNumber2(number);
      setFeedback(`Selected ${number}. Ready to make a move!`);
      if (selectedNumber1 !== null && selectedOperation !== null) {
        try {
          const moveResult = await makeMove(selectedNumber1, number, selectedOperation);
          setHistoryStack((prev) => [...prev, gameState]);
          setGameState(moveResult);
          setSelectedNumber1(null);
          setSelectedNumber2(null);
          setSelectedOperation(null);
          if (moveResult.completed) {
            setFeedback("🎉 Congratulations! You finished the puzzle! 🎉");
            setTimerRunning(false);
          } else {
            setFeedback("Move applied! Select a number to start your next move.");
          }
        } catch (error) {
          console.error('Move failed:', error);
          const errorMessage = error.response?.data?.detail || error.message || 'Move failed';
          setFeedback(errorMessage);
          setSelectedNumber2(null);
          return;
        }
      }
      return;
    }
    if (selectedNumber2 === number) {
      setSelectedNumber2(null);
      setFeedback(`Selected ${selectedNumber1}. Now click an operation.`);
    }
  };

  const handleOperationClick = (operation) => {
    if (selectedNumber1 === null) {
      setFeedback("Please click a number first!");
      return;
    }
    if (selectedOperation === operation) {
      setSelectedOperation(null);
      setFeedback(`Selected ${selectedNumber1}. Now click an operation.`);
      return;
    }
    setSelectedOperation(operation);
    setFeedback(`Selected ${operation}. Now click another number.`);
  };

  const handleUndo = () => {
    if (historyStack.length === 0) {
      setFeedback("No moves to undo!");
      return;
    }
    const prevState = historyStack[historyStack.length - 1];
    setGameState(prevState);
    setHistoryStack((prev) => prev.slice(0, -1));
    setSelectedNumber1(null);
    setSelectedNumber2(null);
    setSelectedOperation(null);
    setFeedback("Move undone!");
  };

  const handleNewGame = async () => {
    const newGame = await getNewGame(difficulty);
    setGameState(newGame);
    setGameId(newGame.game_id);
    setSelectedNumber1(null);
    setSelectedNumber2(null);
    setSelectedOperation(null);
    setFeedback("");
    setHistoryStack([]);
    setTimerRunning(true);
    setElapsedTime(0);
    setTimerKey((k) => k + 1);
  };

  const handleDifficultyChange = (level) => {
    setDifficulty(level);
    getNewGame(level).then((newGame) => {
      setGameState(newGame);
      setGameId(newGame.game_id);
      setSelectedNumber1(null);
      setSelectedNumber2(null);
      setSelectedOperation(null);
      setFeedback("");
      setHistoryStack([]);
      setTimerRunning(true);
      setElapsedTime(0);
      setTimerKey((k) => k + 1);
    });
  };

  return {
    gameState,
    selectedNumber1,
    selectedNumber2,
    selectedOperation,
    feedback,
    difficulty,
    historyStack,
    timerRunning,
    elapsedTime,
    timerKey,
    setElapsedTime,
    handleTimerTick,
    handleNumberClick,
    handleOperationClick,
    handleUndo,
    handleNewGame,
    handleDifficultyChange,
  };
} 