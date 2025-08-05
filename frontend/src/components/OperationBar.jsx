import React from "react";

const operations = ["+", "−", "×", "÷"];

export default function OperationBar({ selectedOperation, onOperationClick, onUndo, canUndo }) {
  return (
    <div className="flex items-center justify-center space-x-4">
      {/* Undo Button */}
      <button 
        className={`btn btn-primary px-4 py-3 ${!canUndo ? 'opacity-50 cursor-not-allowed' : ''}`}
        onClick={onUndo}
        disabled={!canUndo}
      >
        <span className="text-sm font-medium">Undo</span>
      </button>
      
      {/* Operation Buttons */}
      <div className="flex space-x-3">
        {operations.map((op) => (
          <button
            key={op}
            className={`operation-button ${selectedOperation === op ? 'selected' : ''}`}
            onClick={() => onOperationClick(op)}
          >
            {op}
          </button>
        ))}
      </div>
      

    </div>
  );
}