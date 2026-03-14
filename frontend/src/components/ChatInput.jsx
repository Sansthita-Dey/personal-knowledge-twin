import React, { useState, useRef, useEffect } from 'react';
import { Send, Command } from 'lucide-react';

const ChatInput = ({ onSendMessage, disabled }) => {
  const [query, setQuery] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'inherit';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${Math.min(scrollHeight, 150)}px`;
    }
  }, [query]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !disabled) {
      onSendMessage(query.trim());
      setQuery('');

      if (textareaRef.current) {
        textareaRef.current.style.height = 'inherit';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="absolute bottom-0 left-0 right-0 p-4 md:px-12 lg:px-24 bg-gradient-to-t from-background via-background/95 to-transparent pb-6 pt-10 pointer-events-none">
      <div className="max-w-4xl mx-auto pointer-events-auto">

        <form
          onSubmit={handleSubmit}
          className="relative flex items-end gap-2 p-1.5 bg-card border border-primary/20 rounded-3xl shadow-md focus-within:ring-2 ring-primary/40 transition-all duration-300"
        >
          
          {/* Hint icon */}
          <div className="hidden md:flex shrink-0 h-[44px] items-center pl-4 text-primary/60">
            <Command className="w-4 h-4" />
          </div>

          <textarea
            ref={textareaRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Ask NeuroVault anything about your knowledge..."
            className="w-full max-h-[150px] min-h-[44px] py-3 px-3 md:px-2 bg-transparent border-none focus:outline-none text-text placeholder-primary/70 resize-none overflow-y-auto disabled:opacity-50 text-[15px] leading-relaxed"
            rows={1}
          />

          <button
            type="submit"
            disabled={!query.trim() || disabled}
            className="shrink-0 mb-1.5 mr-1.5 w-9 h-9 flex items-center justify-center rounded-2xl bg-primary text-white transition-all disabled:opacity-40 disabled:scale-100 hover:scale-105 active:scale-95 shadow-sm"
          >
            <Send className="w-4 h-4 ml-0.5" />
          </button>

        </form>

        <div className="text-center mt-3">
          <span className="text-xs text-primary/70 font-medium tracking-wide">
            Enter to send, Shift + Enter for new line. Responses are AI-generated.
          </span>
        </div>

      </div>
    </div>
  );
};

export default ChatInput;