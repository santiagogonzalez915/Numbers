import React from "react";

export default function TargetDisplay({ target }) {
  return (
    <div className="target-display">
      <div className="text-base font-semibold opacity-90 mb-2 tracking-wide uppercase">Target Number</div>
      <div className="target-number">
        {target !== undefined && target !== null ? target : "?"}
      </div>
    </div>
  );
}