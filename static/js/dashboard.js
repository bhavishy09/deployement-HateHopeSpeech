document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('sentimentChart');
    
    if (ctx && typeof sentimentData !== 'undefined') {
        const total = sentimentData.positive + sentimentData.neutral + sentimentData.negative;
        
        if (total === 0) {
            ctx.parentElement.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-light);">No predictions yet. Make your first prediction to see analytics!</p>';
            return;
        }
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [sentimentData.positive, sentimentData.neutral, sentimentData.negative],
                    backgroundColor: [
                        'rgba(144, 238, 144, 0.8)',
                        'rgba(255, 217, 102, 0.8)',
                        'rgba(255, 107, 107, 0.8)'
                    ],
                    borderColor: [
                        'rgba(144, 238, 144, 1)',
                        'rgba(255, 217, 102, 1)',
                        'rgba(255, 107, 107, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#2c3e50',
                        bodyColor: '#2c3e50',
                        borderColor: '#e0e0e0',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
});
