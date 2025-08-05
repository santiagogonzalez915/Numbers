import React from "react";

export default function FeedbackBar({ message }) {
  if (!message) return null;
  
  const isSuccess = message.toLowerCase().includes('correct') || 
                   message.toLowerCase().includes('great') || 
                   message.toLowerCase().includes('solved');
  const isError = message.toLowerCase().includes('incorrect') || 
                 message.toLowerCase().includes('wrong') || 
                 message.toLowerCase().includes('error');
  
  return (
    <div className={`feedback-bar ${isSuccess ? 'feedback-success' : isError ? 'feedback-error' : ''}`}>
      <span className="text-lg mr-2">
        {isSuccess ? '✅' : isError ? '❌' : '💡'}
      </span>
      {message}
    </div>
  );
}
