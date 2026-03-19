import React, { useState } from 'react';
import ChatPage from './pages/ChatPage';
import QuizPage from './pages/QuizPage';
import Dashboard from './pages/Dashboard';

const App = () => {
    const [currentPage, setCurrentPage] = useState('chat');

    const renderPage = () => {
        switch (currentPage) {
            case 'chat': return <ChatPage />;
            case 'quiz': return <QuizPage />;
            case 'dashboard': return <Dashboard />;
            default: return <ChatPage />;
        }
    };

    return (
        <div style={{ fontFamily: 'Arial, sans-serif' }}>
            <nav style={{ backgroundColor: '#282c34', padding: '15px 30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: '#fff' }}>
                <h2 style={{ margin: 0 }}>NovaMentor</h2>
                <div style={{ display: 'flex', gap: '20px' }}>
                    <button 
                        onClick={() => setCurrentPage('chat')} 
                        style={{ background: 'none', border: 'none', color: currentPage === 'chat' ? '#61dafb' : '#fff', cursor: 'pointer', fontSize: '16px' }}
                    >
                        Chat
                    </button>
                    <button 
                        onClick={() => setCurrentPage('quiz')} 
                        style={{ background: 'none', border: 'none', color: currentPage === 'quiz' ? '#61dafb' : '#fff', cursor: 'pointer', fontSize: '16px' }}
                    >
                        Quiz
                    </button>
                    <button 
                        onClick={() => setCurrentPage('dashboard')} 
                        style={{ background: 'none', border: 'none', color: currentPage === 'dashboard' ? '#61dafb' : '#fff', cursor: 'pointer', fontSize: '16px' }}
                    >
                        Dashboard
                    </button>
                </div>
            </nav>
            <main>
                {renderPage()}
            </main>
        </div>
    );
};

export default App;
