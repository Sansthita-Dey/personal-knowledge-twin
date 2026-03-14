import React from 'react';
import { Activity } from 'lucide-react';

const Header = ({ status }) => {
  return (
    <header className="h-[72px] shrink-0 border-b border-primary/20 bg-background/80 backdrop-blur-md px-6 flex items-center justify-between z-10 sticky top-0">
      
      <div>
        <h2 className="text-lg font-semibold text-text hidden md:block">
          NeuroVault
        </h2>

        <p className="text-sm text-primary/70 hidden md:block mt-0.5 tracking-wide">
          Your Personal AI Knowledge System
        </p>

        {/* Mobile Title */}
        <h2 className="text-sm font-semibold text-primary md:hidden">
          NeuroVault AI
        </h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-card border border-primary/20">
          
          <Activity className="w-3.5 h-3.5 text-accent" />

          <span className="text-xs font-medium text-text">
            {status}
          </span>

          <span
            className={`w-2 h-2 rounded-full ${
              status === 'Online'
                ? 'bg-green-500'
                : 'bg-primary animate-pulse'
            }`}
          ></span>

        </div>
      </div>

    </header>
  );
};

export default Header;