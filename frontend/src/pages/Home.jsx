import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';
import { fetchChatResponse } from '../services/api';

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (query) => {

    // Add user message immediately
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: query
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const data = await fetchChatResponse(query);

      const aiMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer
      };

      setMessages((prev) => [...prev, aiMsg]);

    } catch (error) {
      console.error("Chat error:", error);

      const errorMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: "⚠️ Something went wrong while contacting the AI."
      };

      setMessages((prev) => [...prev, errorMsg]);

    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden selection:bg-primary/30">
      
      <Sidebar />

      <div className="flex flex-col flex-1 h-full min-w-0 bg-background relative">

        {/* Background glow effects */}
        <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-accent/10 blur-[120px] rounded-full pointer-events-none" />
        <div className="absolute bottom-[20%] right-[-10%] w-[40%] h-[30%] bg-primary/10 blur-[100px] rounded-full pointer-events-none" />

        <Header status={isLoading ? 'Thinking...' : 'Online'} />

        <ChatWindow
          messages={messages}
          isLoading={isLoading}
        />

        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isLoading}
        />

      </div>
    </div>
  );
};

export default Home;