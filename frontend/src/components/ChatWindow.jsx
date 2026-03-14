import React, { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import Loader from './Loader';
import { BrainCircuit } from 'lucide-react';

const ChatWindow = ({ messages, isLoading }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-6 md:px-12 lg:px-24 mb-[90px] scrollbar-thin scrollbar-thumb-primary/40 hover:scrollbar-thumb-primary/60"
      ref={scrollRef}
    >

      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center opacity-90">

          <div className="w-16 h-16 rounded-3xl bg-primary/10 flex items-center justify-center mb-6 ring-1 ring-primary/20">
            <BrainCircuit className="w-8 h-8 text-primary" />
          </div>

          <h2 className="text-2xl font-bold tracking-tight text-text mb-2">
            Welcome to NeuroVault
          </h2>

          <p className="text-primary/70 max-w-sm text-center">
            Your personal AI knowledge system. Feel free to explore your database by asking a question.
          </p>

        </div>
      ) : (
        <div className="flex flex-col max-w-4xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {isLoading && (
            <div className="mb-4">
              <Loader />
            </div>
          )}
        </div>
      )}

    </div>
  );
};

export default ChatWindow;