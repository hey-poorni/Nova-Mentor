import React, { useEffect, useState } from 'react';
import DashboardStats from '../components/DashboardStats';
import { getAnalytics } from '../services/api';

const Dashboard = () => {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        const fetchStats = async () => {
             const result = await getAnalytics();
             setStats(result);
        };
        fetchStats();
    }, []);

    return (
        <div style={{ textAlign: 'center', padding: '20px' }}>
            <h2>Your Learning Dashboard</h2>
            <p style={{ color: '#666', marginBottom: '30px' }}>Track your progress and mastery over time.</p>
            <DashboardStats stats={stats} />
        </div>
    );
};

export default Dashboard;
