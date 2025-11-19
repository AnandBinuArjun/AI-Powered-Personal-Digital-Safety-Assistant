import React, { useState, useEffect } from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = ({ user, onLogout }) => {
  const [riskScore, setRiskScore] = useState(45);
  const [scanHistory, setScanHistory] = useState([
    { id: 1, type: 'URL', content: 'https://suspicious-site.com', result: 'Malicious', date: '2023-05-15' },
    { id: 2, type: 'Message', content: 'You\'ve won $1000!', result: 'Scam', date: '2023-05-14' },
    { id: 3, type: 'Email', content: 'user@example.com', result: 'Safe', date: '2023-05-13' },
  ]);
  const [platformInsights, setPlatformInsights] = useState({
    android: { scans: 15, risks: 0.3 },
    web: { scans: 8, risks: 0.2 },
    browserExtension: { scans: 12, risks: 0.4 }
  });
  const [recommendations, setRecommendations] = useState([
    "Review your accounts for data breaches and change passwords",
    "Be cautious when clicking links, especially in emails or messages"
  ]);

  const riskData = {
    labels: ['Breach Risk', 'Malicious URLs', 'Suspicious Messages', 'Password Risk'],
    datasets: [
      {
        label: 'Risk Factors',
        data: [30, 20, 60, 10],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const platformData = {
    labels: ['Android', 'Web', 'Browser Extension'],
    datasets: [
      {
        label: 'Risk Distribution',
        data: [
          platformInsights.android.risks * 100,
          platformInsights.web.risks * 100,
          platformInsights.browserExtension.risks * 100
        ],
        backgroundColor: [
          'rgba(255, 159, 64, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
        borderColor: [
          'rgba(255, 159, 64, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 1,
      },
    ],
  };

  const scoreData = {
    labels: ['Your Score'],
    datasets: [
      {
        label: 'Safety Score',
        data: [riskScore],
        backgroundColor: riskScore > 70 ? 'rgba(255, 99, 132, 0.6)' : 
                       riskScore > 40 ? 'rgba(255, 206, 86, 0.6)' : 
                       'rgba(75, 192, 192, 0.6)',
        borderColor: riskScore > 70 ? 'rgba(255, 99, 132, 1)' : 
                      riskScore > 40 ? 'rgba(255, 206, 86, 1)' : 
                      'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const scoreOptions = {
    scales: {
      y: {
        min: 0,
        max: 100,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Safety Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.name}</span>
          <button onClick={onLogout} className="logout-button">Logout</button>
        </div>
      </header>

      <main className="dashboard-content">
        <section className="score-section">
          <h2>Your Cyber Safety Score</h2>
          <div className="score-container">
            <div className="score-chart">
              <Bar data={scoreData} options={scoreOptions} />
            </div>
            <div className="score-details">
              <div className={`score-badge ${riskScore > 70 ? 'high' : riskScore > 40 ? 'medium' : 'low'}`}>
                {riskScore}/100
              </div>
              <p className="score-description">
                {riskScore > 70 
                  ? 'High risk detected. Take immediate action to improve your security.' 
                  : riskScore > 40 
                  ? 'Moderate risk. Review your security practices.' 
                  : 'Good security practices. Keep up the good work!'}
              </p>
            </div>
          </div>
        </section>

        <section className="charts-section">
          <div className="chart-container">
            <h3>Risk Factors</h3>
            <Doughnut data={riskData} />
          </div>
          <div className="chart-container">
            <h3>Platform Insights</h3>
            <Doughnut data={platformData} />
          </div>
        </section>

        <section className="recommendations-section">
          <h3>Personalized Recommendations</h3>
          <ul className="recommendations-list">
            {recommendations.map((rec, index) => (
              <li key={index} className="recommendation-item">{rec}</li>
            ))}
          </ul>
        </section>

        <section className="history-section">
          <h3>Recent Scans</h3>
          <table className="scan-history">
            <thead>
              <tr>
                <th>Type</th>
                <th>Content</th>
                <th>Result</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {scanHistory.map((scan) => (
                <tr key={scan.id}>
                  <td>{scan.type}</td>
                  <td>{scan.content}</td>
                  <td className={scan.result.toLowerCase()}>{scan.result}</td>
                  <td>{scan.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;