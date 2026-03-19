import React, { useState } from 'react';
import QuizCard from '../components/QuizCard';
import { getQuiz } from '../services/api';

const QuizPage = () => {
    const [topic, setTopic] = useState('');
    const [quiz, setQuiz] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleGenerate = async () => {
        if (!topic.trim()) return;
        setLoading(true);
        setQuiz(null); // Clear previous quiz
        const result = await getQuiz(topic);
        if (result && !result.error) {
            setQuiz(result);
        } else {
            alert(result.error || "Something went wrong.");
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <h2>Dynamic Quiz Generator</h2>
            <div style={{ margin: '30px auto' }}>
                <input 
                    type="text" 
                    value={topic} 
                    onChange={(e) => setTopic(e.target.value)} 
                    placeholder="Enter topic (e.g., binary search)" 
                    style={{ padding: '10px', width: '250px', borderRadius: '4px', border: '1px solid #ddd' }}
                />
                <button 
                    onClick={handleGenerate} 
                    disabled={loading}
                    style={{ marginLeft: '10px', padding: '10px 20px', backgroundColor: '#3f51b5', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    {loading ? 'Generating...' : 'Generate Quiz'}
                </button>
            </div>
            {quiz && <QuizCard quizData={quiz} />}
        </div>
    );
};

export default QuizPage;
