import React, { useState, useEffect, useRef } from 'react';

export default function Support() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [status, setStatus] = useState('Disconnected'); // 'Connecting' | 'Connected' | 'Disconnected'
  const ws = new WebSocket('ws://localhost:8000/ws/support/'); //FIXME link

  const socketRef = useRef(null);
  const chatEndRef = useRef(null);

  // Auto-scroll message list when new messages arrive
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSocket = () => {
    if (!isOpen) return;

    setStatus('Connecting');
    // Standard Browser WebSocket instantiation
    socketRef.current = ws;

    ws.onopen = () => {
      setStatus('Connected');
    };

    // Strictly process incoming backend messages
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + Math.random(),
            sender: data.sender || 'agent',
            message: data.message || '',
            timestamp:
              data.timestamp ||
              new Date().toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              }),
          },
        ]);
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = () => setStatus('Disconnected');
    ws.onclose = () => setStatus('Disconnected');
  };

  // Connect to Django WebSocket backend
  useEffect(() => {
    handleSocket();

    return () => {
      ws.close();
    };
  }, [isOpen]);

  // Send message over WebSocket
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const text = inputValue.trim();
    const timestamp = new Date().toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });

    // 1. Optimistically append user message to state
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), sender: 'user', message: text, timestamp },
    ]);

    // 2. Dispatch structured payload to Django Channels consumer
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ message: text, sender: 'user' }));
    }

    setInputValue('');
  };

  // Manual trigger for testing incoming backend frames without automatic timers
  const simulateBackendPush = () => {
    const mockEvent = {
      data: JSON.stringify({
        sender: 'agent',
        message: 'Hello! This is a manual test push from the server.',
        timestamp: new Date().toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        }),
      }),
    };
    if (socketRef.current?.onmessage) {
      socketRef.current.onmessage(mockEvent);
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50 font-sans text-slate-800 dark:text-slate-100">
      {/* Floating Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-full shadow-lg transition-all transform hover:scale-105"
        >
          <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
          </svg>
          <span className="text-sm font-semibold">Support</span>
        </button>
      )}

      {/* Main Chat Container */}
      {isOpen && (
        <div className="w-[calc(100vw-2.5rem)] sm:w-96 h-[500px] bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-slate-900 text-white px-4 py-3 flex items-center justify-between shrink-0">
            <div className="flex items-center space-x-2.5">
              <span
                className={`w-2.5 h-2.5 rounded-full ${
                  status === 'Connected'
                    ? 'bg-emerald-500'
                    : status === 'Connecting'
                      ? 'bg-amber-500 animate-pulse'
                      : 'bg-rose-500'
                }`}
              />
              <span className="text-xs font-semibold tracking-wide">
                Support Chat
              </span>
            </div>

            <div className="flex items-center space-x-2">
              {/* Manual Debug Push Button */}
              <button
                type="button"
                onClick={simulateBackendPush}
                title="Simulate incoming WebSocket push from backend"
                className="text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded border border-slate-700"
              >
                + Test Push
              </button>

              {/* Close Widget */}
              <button
                onClick={() => setIsOpen(false)}
                className="text-slate-400 hover:text-white p-1 text-sm font-bold leading-none"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Message Stream */}
          <div className="flex-1 p-3 overflow-y-auto space-y-2 bg-slate-50 dark:bg-slate-950">
            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400 text-center px-4">
                Connected to server. Send a message to get started.
              </div>
            ) : (
              messages.map((msg) => {
                const isUser = msg.sender === 'user';
                return (
                  <div
                    key={msg.id}
                    className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-[80%] px-3 py-2 rounded-xl text-xs leading-relaxed ${
                        isUser
                          ? 'bg-blue-600 text-white rounded-br-none'
                          : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-700/60 rounded-bl-none shadow-xs'
                      }`}
                    >
                      {msg.message}
                    </div>
                    {msg.timestamp && (
                      <span className="text-[9px] text-slate-400 mt-0.5 px-1">
                        {msg.timestamp}
                      </span>
                    )}
                  </div>
                );
              })
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Input Form */}
          <form
            onSubmit={handleSendMessage}
            className="p-2.5 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex space-x-2 shrink-0"
          >
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-xs rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500 placeholder-slate-400"
            />
            <button
              type="submit"
              disabled={!inputValue.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs px-3.5 py-2 rounded-lg font-medium transition-colors"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
