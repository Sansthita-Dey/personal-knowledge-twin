import React from 'react';
import { User, Sparkles } from 'lucide-react';

const MessageBubble = ({ message }) => {
  const isAI = message.role === 'assistant';

  return (
    <div className={`flex w-full ${isAI ? 'justify-start' : 'justify-end'} mb-6 group`}>
      <div className={`flex max-w-[85%] md:max-w-[75%] gap-4 ${isAI ? 'flex-row' : 'flex-row-reverse'}`}>
        
        {/* Avatar */}
        <div className="shrink-0 flex items-start">
          <div className={`w-9 h-9 rounded-xl flex items-center justify-center shadow-md border ${
            isAI 
              ? 'bg-gradient-to-br from-primary to-accent border-primary/20' 
              : 'bg-primary/20 border-primary/30'
          }`}>
            {isAI ? (
              <Sparkles className="w-5 h-5 text-white" />
            ) : (
              <User className="w-5 h-5 text-primary" />
            )}
          </div>
        </div>

        {/* Message Content */}
        <div className={`flex flex-col gap-1.5 mt-1 ${isAI ? 'items-start' : 'items-end'}`}>
          
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold text-text">
              {isAI ? 'NeuroVault' : 'You'}
            </span>
          </div>
          
          <div className={`relative px-5 py-4 rounded-2xl text-[15px] shadow-sm leading-relaxed ${
            isAI 
              ? 'bg-card border border-primary/10 text-text rounded-tl-sm' 
              : 'bg-primary border border-primary text-white rounded-tr-sm'
          }`}>
            {message.content}

            {/* subtle highlight for AI responses */}
            {isAI && (
              <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-accent/5 rounded-2xl pointer-events-none" />
            )}
          </div>

        </div>

      </div>
    </div>
  );
};

export default MessageBubble;