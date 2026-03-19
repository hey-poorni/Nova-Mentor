import React, { useState } from 'react';

const QuizCard = ({ quizData }) => {
    const [selected, setSelected] = useState(null);
    const [showAnswer, setShowAnswer] = useState(false);

    if (!quizData) return null;

    const handleOptionSelect = (option) => {
        setSelected(option);
        setShowAnswer(true);
    };

    const isCorrect = selected === quizData.answer;

    return (
        <div style={{ border: '1px solid #ddd', padding: '20px', borderRadius: '8px', maxWidth: '500px', margin: '20px auto' }}>
            <h3>{quizData.question}</h3>
            <div style={{ display: 'grid', gap: '10px', marginTop: '15px' }}>
                {quizData.options.map((opt, idx) => (
                    <button 
                        key={idx} 
                        onClick={() => !showAnswer && handleOptionSelect(opt)}
                        style={{ 
                            padding: '10px', 
                            cursor: showAnswer ? 'default' : 'pointer',
                            backgroundColor: showAnswer && opt === quizData.answer ? '#c8e6c9' : (showAnswer && opt === selected ? '#ffcdd2' : '#fff'),
                            borderColor: showAnswer && opt === quizData.answer ? '#4caf50' : '#ddd',
                            borderStyle: 'solid',
                            borderWidth: '1px'
                        }}
                        disabled={showAnswer}
                    >
                        {opt}
                    </button>
                ))}
            </div>

            {showAnswer && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: isCorrect ? '#e8f5e9' : '#fff3e0' }}>
                    <strong>{isCorrect ? '✓ Correct!' : '✗ Incorrect'}</strong>
                    <p style={{ marginTop: '5px' }}><strong>Explanation:</strong> {quizData.explanation}</p>
                </div>
            )}
        </div>
    );
};

export default QuizCard;
