import React from 'react';
import { BrainCircuit, MessageSquare, Plus, Settings, Database } from 'lucide-react';

const Sidebar = () => {
  return (
    <aside className="w-[280px] h-full flex flex-col bg-background border-r border-primary/20 p-4 shrink-0 transition-all duration-300">
      
      {/* Logo Area */}
      <div className="flex items-center gap-3 px-2 py-4 mb-6">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg border border-primary/20">
          <BrainCircuit className="w-5 h-5 text-white" />
        </div>

        <div>
          <h1 className="text-xl font-bold text-text tracking-tight">
            NeuroVault
          </h1>
        </div>
      </div>

      {/* New Chat Button */}
      <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-primary/10 hover:bg-primary/20 border border-primary/20 text-text font-medium transition-all duration-200 group">
        <Plus className="w-5 h-5 text-primary group-hover:scale-110 transition-transform" />
        New Chat
      </button>

      {/* Navigation / History */}
      <div className="flex-1 overflow-y-auto mt-8 scrollbar-hide py-2">
        <h3 className="text-xs font-semibold text-primary uppercase tracking-wider mb-4 px-2">
          Knowledge Space
        </h3>
        
        <div className="space-y-1">
          <NavItem icon={<Database className="w-4 h-4" />} label="Knowledge Base" active={false} />
          <NavItem icon={<MessageSquare className="w-4 h-4" />} label="Recent Chats" active={true} />
        </div>
      </div>

      {/* Settings */}
      <div className="mt-auto pt-4 border-t border-primary/20">
        <NavItem icon={<Settings className="w-4 h-4" />} label="Settings" active={false} />
      </div>

    </aside>
  );
};

const NavItem = ({ icon, label, active }) => (
  <button 
    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
      active 
        ? 'bg-primary/10 text-text' 
        : 'text-text/70 hover:bg-primary/10 hover:text-text'
    }`}
  >
    {icon}
    {label}
  </button>
);

export default Sidebar;