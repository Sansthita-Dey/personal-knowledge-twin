import React from 'react';

const Loader = () => {
  return (
    <div className="flex items-center gap-2 px-4 py-3 max-w-[fit-content] rounded-2xl bg-slate-800/60 border border-slate-700/50 backdrop-blur-sm self-start">
      <div className="flex gap-1.5 items-center">
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
        <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
      </div>
      <span className="text-sm text-slate-400 ml-2 font-medium tracking-wide">Retrieving from Vault...</span>
    </div>
  );
};

export default Loader;
