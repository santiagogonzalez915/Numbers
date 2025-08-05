import React from "react";

export default function DifficultySelector({ difficulty, onChange }) {
  const levels = [
    { label: "Easy", value: 1 },
    { label: "Medium", value: 2 },
    { label: "Hard", value: 3 },
  ];

  return (
    <select 
      value={difficulty} 
      onChange={(e) => onChange(parseInt(e.target.value))}
      className="input text-sm"
    >
      {levels.map(({ label, value }) => (
        <option key={value} value={value}>
          {label}
        </option>
      ))}
    </select>
  );
}
