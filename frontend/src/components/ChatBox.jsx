import React, { useState } from 'react';
import { sendMessage } from '../services/api';

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;
        
        const userMsg = { text: input, role: 'user' };
        setMessages([...messages, userMsg]);
        setInput('');
        setLoading(true);

        const result = await sendMessage(input);
        const aiMsg = { text: result.reply, role: 'ai' };
        setMessages(prev => [...prev, aiMsg]);
        setLoading(false);
    };

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
            <div style={{ border: '1px solid #ddd', padding: '10px', minHeight: '300px', overflowY: 'auto' }}>
                {messages.map((m, idx) => (
                    <div key={idx} style={{ marginBottom: '10px', textAlign: m.role === 'user' ? 'right' : 'left' }}>
                        <strong>{m.role === 'user' ? 'You' : 'Nova'}:</strong>
                        <p style={{ display: 'inline-block', backgroundColor: m.role === 'user' ? '#e1f5fe' : '#f5f5f5', padding: '8px', borderRadius: '10px' }}>
                            {m.text}
                        </p>
                    </div>
                ))}
            </div>
            <div style={{ marginTop: '10px' }}>
                <input 
                    type="text" 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)} 
                    placeholder="Type your message..."
                    style={{ width: '80%', padding: '8px' }}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />
                <button onClick={handleSend} disabled={loading} style={{ width: '18%', padding: '8px', cursor: 'pointer' }}>
                    {loading ? 'Thinking...' : 'Send'}
                </button>
            </div>
        </div>
    );
};

export default ChatBox;
