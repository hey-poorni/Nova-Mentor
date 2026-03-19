import React from 'react';
import ChatBox from '../components/ChatBox';

const ChatPage = () => {
    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <h2>Nova Socratic Assistant</h2>
            <p style={{ color: '#666', marginBottom: '30px' }}>Ask Nova anything. It will guide you through step-by-step thinking.</p>
            <ChatBox />
        </div>
    );
};

export default ChatPage;
