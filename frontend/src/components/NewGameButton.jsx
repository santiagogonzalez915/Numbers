import React from "react";
import newGameImg from "../assets/new_game.png";

export default function NewGameButton({ onClick }) {
  return (
    <button
      className="w-full min-w-[8rem] rounded-xl bg-white hover:bg-indigo-50 text-indigo-700 font-semibold uppercase py-3 mt-4 shadow-lg transition-colors duration-150 border-2 border-indigo-400 flex items-center justify-center text-base tracking-wide"
      onClick={onClick}
    >
      <img src={newGameImg} alt="New Game" className="h-10 w-auto object-contain" />
    </button>
  );
}
