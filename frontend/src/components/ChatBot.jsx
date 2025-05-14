import React, { useState } from 'react';
import axios from 'axios';

const ChatBot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm AgriAI Assistant. How can I help with your farming questions today?", isBot: true }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Add user message
    const userMessage = { text: input, isBot: false };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Make API call to the backend
      const response = await axios.post('http://127.0.0.1:8000/chatbot', { 
        message: input 
      });
      
      // Add bot response
      setMessages(prev => [...prev, { 
        text: response.data.response || "Sorry, I couldn't process that request.", 
        isBot: true 
      }]);
    } catch (error) {
      console.error('Error communicating with chatbot:', error);
      setMessages(prev => [...prev, { 
        text: "I'm having trouble connecting right now. Please try again later.", 
        isBot: true 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">🌿 AgriAI Assistant</h1>
      
      {/* Chat messages */}
      <div className="bg-gray-100 p-4 h-96 overflow-y-auto rounded mb-4">
        {messages.map((msg, index) => (
          <div 
            key={index} 
            className={`mb-3 p-3 rounded-lg ${
              msg.isBot 
                ? 'bg-green-100 text-green-900' 
                : 'bg-blue-100 text-blue-900 ml-auto'
            } ${msg.isBot ? 'mr-12' : 'ml-12'} max-w-xs md:max-w-md`}
          >
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="bg-green-100 text-green-900 p-3 rounded-lg mb-3 mr-12 max-w-xs">
            Thinking...
          </div>
        )}
      </div>
      
      {/* Input area */}
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask about crops, diseases, or farming practices..."
          className="flex-grow p-2 border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="bg-green-600 text-white px-4 py-2 rounded-r hover:bg-green-700 disabled:bg-gray-400"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBot;