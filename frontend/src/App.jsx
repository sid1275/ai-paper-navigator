import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'http://127.0.0.1:8000';

// --- NEW Source Component ---
const Source = ({ source, index }) => {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="source">
      <button onClick={() => setIsOpen(!isOpen)} className="source-button">
        {isOpen ? 'Hide' : 'Show'} Source {index + 1} (Page {source.page})
      </button>
      {isOpen && <div className="source-content">{source.content}</div>}
    </div>
  );
};

function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsReady(false);
    setMessages([]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setMessages([{ sender: 'system', text: `Processing ${selectedFile.name}...` }]);
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      await axios.post(`${API_URL}/upload_pdf/`, formData);
      setMessages([{ sender: 'system', text: `Ready! Ask me anything about ${selectedFile.name}.` }]);
      setIsReady(true);
    } catch (error) {
      setMessages([{ sender: 'system', text: 'Error processing PDF. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!userInput.trim() || !isReady) return;
    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);
    const question = userInput;
    setUserInput('');
    setIsLoading(true);
    try {
      const response = await axios.post(`${API_URL}/ask/`, { question });
      // --- MODIFIED ---
      // The bot's message now includes the answer and the sources
      setMessages([...newMessages, { 
        sender: 'bot', 
        text: response.data.answer,
        sources: response.data.sources 
      }]);
    } catch (error) {
      setMessages([...newMessages, { sender: 'bot', text: 'Sorry, I encountered an error.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="header"><h2>AI Paper Navigator 💡</h2></div>
        <div className="messages-area">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.sender}`}>
              <div className={`message ${msg.sender}`}><p>{msg.text}</p></div>
              {/* --- NEW --- Render sources if they exist */}
              {msg.sources && (
                <div className="sources-container">
                  {msg.sources.map((source, s_index) => (
                    <Source key={s_index} source={source} index={s_index} />
                  ))}
                </div>
              )}
            </div>
          ))}
          {isLoading && <div className="message bot"><p>Thinking...</p></div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="bottom-area">
          {isReady ? (
            <div className="input-area">
              <input type="text" value={userInput} onChange={(e) => setUserInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()} placeholder="Ask a question..." disabled={isLoading} />
              <button onClick={handleSendMessage} disabled={isLoading}>Send</button>
            </div>
          ) : (
            <div className="upload-area">
              <input type="file" accept=".pdf" onChange={handleFileChange} />
              <button onClick={handleFileUpload} disabled={!selectedFile || isLoading}>Upload & Process</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;