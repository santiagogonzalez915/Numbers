import React from "react";

export default function NumbersGrid({ numbers, selectedNumber1, selectedNumber2, onNumberClick }) {
  return (
    <div className="numbers-grid">
      {numbers.map((num, idx) => {
        const isSelected = num === selectedNumber1 || num === selectedNumber2;
        return (
          <button
            key={idx}
            className={`number-button animate-scale-in ${isSelected ? 'selected' : ''}`}
            style={{ animationDelay: `${0.2 + idx * 0.1}s` }}
            onClick={() => onNumberClick(num)}
          >
            {num}
          </button>
        );
      })}
    </div>
  );
}
