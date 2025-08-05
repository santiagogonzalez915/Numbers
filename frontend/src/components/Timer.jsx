import React, { useEffect, useRef, useState } from "react";

export default function Timer({ running, onComplete, onReset, onTick }) {
  const [seconds, setSeconds] = useState(0);
  const intervalRef = useRef(null);
  const prevRunning = useRef(running);

  useEffect(() => {
    if (running) {
      if (!intervalRef.current) {
        intervalRef.current = setInterval(() => {
          setSeconds((s) => {
            const newSeconds = s + 1;
            if (onTick) {
              onTick(newSeconds);
            }
            return newSeconds;
          });
        }, 1000);
      }
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
        if (prevRunning.current && onComplete) {
          onComplete(seconds);
        }
      }
    }
    prevRunning.current = running;
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [running]);

  useEffect(() => {
    if (!running) {
      setSeconds(0);
      if (onReset) onReset();
    }
  }, [running === false]);

  const pad = (n) => n.toString().padStart(2, "0");
  const mins = pad(Math.floor(seconds / 60));
  const secs = pad(seconds % 60);

  return (
    <div className="timer">
      <span className="text-blue-300 text-medium font-medium">Time:</span>
      <span className="ml-2 font-mono text-medium text-cyan-300">{mins}:{secs}</span>
    </div>
  );
} 