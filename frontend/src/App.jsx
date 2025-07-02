import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// The URL for our FastAPI backend
const API_URL = 'http://127.0.0.1:8000';

function App() {
  // State variables to manage the component's data
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false); // Is the app ready to chat?

  // A ref to automatically scroll to the latest message
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // This effect runs whenever the 'messages' array changes
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // --- HANDLER FUNCTIONS ---

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert('Please select a PDF file first.');
      return;
    }
    setIsLoading(true);
    setMessages([{ sender: 'system', text: `Processing ${selectedFile.name}...` }]);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post(`${API_URL}/upload_pdf/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setMessages([{ sender: 'system', text: `Ready! Ask me anything about ${selectedFile.name}.` }]);
      setIsReady(true);
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessages([{ sender: 'system', text: 'Error processing PDF. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!userInput.trim() || !isReady) return;

    const newMessages = [...messages, { sender: 'user', text: userInput }];
    setMessages(newMessages);
    setUserInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/ask/`, { question: userInput });
      setMessages([...newMessages, { sender: 'bot', text: response.data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages([...newMessages, { sender: 'bot', text: 'Sorry, I encountered an error.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  // --- RENDER ---
  
  return (
    <div className="App">
      <div className="chat-container">
        <div className="header">
          <h2>AI Paper Navigator</h2>
        </div>
        
        <div className="messages-area">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.sender}`}>
              <p>{msg.text}</p>
            </div>
          ))}
          {isLoading && <div className="message bot"><p>Thinking...</p></div>}
          <div ref={messagesEndRef} />
        </div>

        {isReady ? (
          <div className="input-area">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <button onClick={handleSendMessage} disabled={isLoading}>
              Send
            </button>
          </div>
        ) : (
          <div className="upload-area">
            <input type="file" accept=".pdf" onChange={handleFileChange} />
            <button onClick={handleFileUpload} disabled={isLoading}>
              Upload and Process PDF
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;