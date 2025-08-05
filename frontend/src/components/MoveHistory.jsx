import React from "react";

export default function MoveHistory({ history }) {
  return (
    <div className="p-4 border border-slate-200 rounded-lg bg-white">
      <h3 className="font-semibold text-slate-700 mb-3 text-lg text-center">Move History</h3>
      <div className="space-y-2">
        {history && history.length > 0 ? (
          history.map((move, idx) => (
            <div key={idx} className="flex items-center justify-center p-3 bg-gray-50 rounded-lg border border-slate-200">
              <span className="font-mono text-slate-800 font-semibold text-center">{move.replace(/\*/g, '×')}</span>
            </div>
          ))
        ) : (
          <div className="p-3 bg-gray-50 rounded-lg border border-slate-200">
            <span className="text-sm text-slate-500 italic text-center block">No moves yet</span>
          </div>
        )}
      </div>
    </div>
  );
}
