import React, { useState, useEffect, useCallback, useRef } from 'react';

interface Message {
  id: number;
  body: string;
  timestamp: string;
}

// Simulate a WebSocket connection for receiving messages
// In a real app, this would connect to a backend service
// that consumes RabbitMQ messages and forwards them via WebSocket.
const useMockWebSocket = (
  onMessage: (message: Message) => void,
  isConsuming: boolean
) => {
  const messageCounter = useRef(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isConsuming) {
      console.log('Mock WebSocket: Starting message simulation...');
      intervalRef.current = setInterval(() => {
        const newMessage: Message = {
          id: messageCounter.current++,
          body: `Simulated message #${messageCounter.current} content. Lorem ipsum dolor sit amet.`,
          timestamp: new Date().toLocaleTimeString(),
        };
        onMessage(newMessage);
      }, 2000); // Simulate receiving a message every 2 seconds
    } else {
      console.log('Mock WebSocket: Stopping message simulation.');
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    // Cleanup function
    return () => {
      console.log('Mock WebSocket: Cleaning up interval.');
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isConsuming, onMessage]);

  // Simulate connection status change
  const [isConnected, setIsConnected] = useState(false);
  useEffect(() => {
    // Simulate connection delay
    const connectTimeout = setTimeout(() => {
        setIsConnected(true);
        console.log('Mock WebSocket: Connected.');
    }, 1000);

    // Simulate disconnection possibility (e.g., on component unmount)
    return () => {
        clearTimeout(connectTimeout);
        setIsConnected(false);
        console.log('Mock WebSocket: Disconnected.');
    };
  }, []);


  return { isConnected };
};

const RabbitMQConsumerDisplay: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConsuming, setIsConsuming] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleNewMessage = useCallback((newMessage: Message) => {
    setMessages((prevMessages) => [...prevMessages, newMessage].slice(-100)); // Keep last 100 messages
  }, []);

  const { isConnected } = useMockWebSocket(handleNewMessage, isConsuming);

   useEffect(() => {
    // Auto-scroll to the bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);


  const startConsumption = () => {
    if (isConnected) {
        console.log("Starting consumption...");
        setIsConsuming(true);
    } else {
        console.log("Cannot start consumption: Not connected.");
        // Optionally show an error message to the user
    }
  };

  const stopConsumption = () => {
    console.log("Stopping consumption...");
    setIsConsuming(false);
  };

  const clearMessages = () => {
    console.log("Clearing messages...");
    setMessages([]);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-6 font-sans">
      <header className="mb-6 pb-4 border-b border-gray-300">
        <h1 className="text-3xl font-bold text-gray-800">RabbitMQ Message Consumer</h1>
        <p className="text-sm text-gray-600 mt-1">Displays messages received from a (simulated) RabbitMQ queue.</p>
      </header>

      <div className="flex items-center justify-between mb-4 p-4 bg-white rounded-lg shadow">
        <div className="flex items-center space-x-3">
           <span className={`h-3 w-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></span>
           <span className="text-gray-700 font-medium">
             Status: {isConnected ? 'Connected' : 'Disconnected'} {isConsuming && isConnected ? '(Consuming)' : ''} {!isConsuming && isConnected ? '(Paused)' : ''}
           </span>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={startConsumption}
            disabled={isConsuming || !isConnected}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
              isConsuming || !isConnected
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            Start Consuming
          </button>
          <button
            onClick={stopConsumption}
            disabled={!isConsuming}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 ${
              !isConsuming
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-yellow-500 hover:bg-yellow-600'
            }`}
          >
            Stop Consuming
          </button>
          <button
            onClick={clearMessages}
            disabled={messages.length === 0}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 ${
              messages.length === 0
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-red-500 hover:bg-red-600'
            }`}
          >
            Clear Messages
          </button>
        </div>
      </div>

      <div className="flex-grow bg-white rounded-lg shadow overflow-hidden">
        <div className="h-full overflow-y-auto p-4 space-y-3">
          {messages.length === 0 && (
            <div className="flex items-center justify-center h-full text-gray-500">
              {isConnected ? 'Waiting for messages...' : 'Disconnected. Cannot receive messages.'}
            </div>
          )}
          {messages.map((msg) => (
            <div key={msg.id} className="p-3 bg-gray-50 rounded-md border border-gray-200 shadow-sm">
              <div className="flex justify-between items-center mb-1">
                <span className="text-xs font-semibold text-blue-700">Message #{msg.id}</span>
                <span className="text-xs text-gray-500">{msg.timestamp}</span>
              </div>
              <p className="text-sm text-gray-800 break-words">{msg.body}</p>
            </div>
          ))}
           <div ref={messagesEndRef} /> {/* Anchor for scrolling */}
        </div>
      </div>
       <footer className="mt-6 pt-4 text-center text-xs text-gray-500 border-t border-gray-300">
         Note: This is a frontend simulation. A real implementation requires a backend service to connect to RabbitMQ.
       </footer>
    </div>
  );
};

export default RabbitMQConsumerDisplay;
