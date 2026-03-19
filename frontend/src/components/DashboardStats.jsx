import React from 'react';

const DashboardStats = ({ stats }) => {
    if (!stats) return <p>Loading stats...</p>;

    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '12px', margin: '20px auto', maxWidth: '800px' }}>
            <div style={{ padding: '15px', backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', borderRadius: '8px', textAlign: 'center' }}>
                <h4 style={{ color: '#555', marginBottom: '8px' }}>Total Attempts</h4>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#333' }}>{stats.total_attempts}</p>
            </div>
            
            <div style={{ padding: '15px', backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', borderRadius: '8px', textAlign: 'center' }}>
                <h4 style={{ color: '#555', marginBottom: '8px' }}>Accuracy</h4>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#4caf50' }}>{stats.accuracy}%</p>
            </div>

            <div style={{ padding: '15px', backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', borderRadius: '8px', textAlign: 'center' }}>
                <h4 style={{ color: '#555', marginBottom: '8px' }}>Correct</h4>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#2196f3' }}>{stats.correct_answers}</p>
            </div>

            <div style={{ padding: '15px', backgroundColor: '#fff', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', borderRadius: '8px', textAlign: 'center' }}>
                <h4 style={{ color: '#555', marginBottom: '8px' }}>Incorrect</h4>
                <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#f44336' }}>{stats.incorrect_answers}</p>
            </div>
        </div>
    );
};

export default DashboardStats;
