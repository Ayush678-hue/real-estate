import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, User, Loader } from 'lucide-react';
import { aiService } from '../api';
import './AIChatbot.css';

const AIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'model', content: 'Hi! I am your real estate AI assistant. How can I help you find your dream property today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await aiService.chat(userMessage, sessionId);
      setSessionId(response.data.session_id);
      
      let aiReply = response.data.reply;
      
      setMessages(prev => [...prev, { 
        role: 'model', 
        content: aiReply,
        properties: response.data.properties
      }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev => [...prev, { 
        role: 'model', 
        content: 'Sorry, I encountered an error connecting to the AI service. Please try again later.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
      {/* Floating Button */}
      {!isOpen && (
        <button 
          className="chatbot-trigger btn-primary"
          onClick={() => setIsOpen(true)}
        >
          <Bot size={24} />
          <span className="tooltip">Ask AI</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window glass-card animate-fade-in">
          <div className="chat-header">
            <div className="chat-title">
              <Bot className="brand-icon" size={20} />
              <span>Estate<span className="gradient-text">AI</span> Assistant</span>
            </div>
            <button className="icon-btn" onClick={() => setIsOpen(false)}>
              <X size={20} />
            </button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-wrapper ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'model' ? <Bot size={16} /> : <User size={16} />}
                </div>
                <div className={`message-bubble ${msg.role}`}>
                  <p>{msg.content}</p>
                  
                  {/* Render suggested properties if any */}
                  {msg.properties && msg.properties.length > 0 && (
                    <div className="suggested-properties">
                      {msg.properties.map(prop => (
                        <div key={prop.id} className="suggested-property glass">
                          <div className="sp-price">₹{Number(prop.price).toLocaleString('en-IN')}</div>
                          <div className="sp-title">{prop.title}</div>
                          <div className="sp-meta">{prop.bedrooms} Bed • {prop.city}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message-wrapper model">
                <div className="message-avatar"><Bot size={16} /></div>
                <div className="message-bubble model typing">
                  <Loader className="spin" size={16} /> Thinking...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-input-area" onSubmit={handleSend}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about properties in Mumbai..."
              className="chat-input"
              disabled={loading}
            />
            <button type="submit" className="chat-send-btn" disabled={!input.trim() || loading}>
              <Send size={18} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default AIChatbot;
