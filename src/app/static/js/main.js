// Estado global de la aplicación
let currentUserId = null;
let currentRecommendation = null;
let availableUsers = [];

// Utilidades
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showError(message) {
    alert('Error: ' + message);
}

function formatPercentage(value) {
    return Math.round(value * 100) + '%';
}

function formatNumber(value, decimals = 2) {
    return Number(value).toFixed(decimals);
}

// Cargar usuarios disponibles
async function loadAvailableUsers() {
    try {
        showLoading();
        const response = await fetch('/api/users?limit=100');
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        availableUsers = data.users;
        
        const select = document.getElementById('userSelect');
        select.innerHTML = '<option value="">Selecciona un usuario...</option>';
        
        data.users.forEach(userId => {
            const option = document.createElement('option');
            option.value = userId;
            option.textContent = `Usuario ${userId}`;
            select.appendChild(option);
        });
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error cargando usuarios: ' + error.message);
    }
}

// Cargar estado del usuario
async function loadUserState(userId) {
    try {
        showLoading();
        const response = await fetch(`/api/users/${userId}/state`);
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        currentUserId = userId;
        
        // Mostrar secciones
        document.getElementById('userStateSection').style.display = 'block';
        document.getElementById('recommendationSection').style.display = 'block';
        document.getElementById('userProfileSection').style.display = 'block';
        
        // Actualizar ID del usuario
        document.getElementById('currentUserId').textContent = `#${userId}`;
        
        // Actualizar barras de progreso
        updateProgressBar('musicEngagement', data.music_engagement);
        updateProgressBar('musicDiversity', data.music_diversity);
        updateProgressBar('socialConnectivity', data.social_connectivity);
        updateProgressBar('semanticActivity', data.semantic_activity);
        updateProgressBar('overallSophistication', data.overall_sophistication);
        
        // Cargar perfil del usuario
        await loadUserProfile(userId);
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error cargando estado del usuario: ' + error.message);
    }
}

function updateProgressBar(id, value) {
    const fill = document.getElementById(id);
    const valueSpan = document.getElementById(id + 'Value');
    
    const percentage = Math.round(value * 100);
    fill.style.width = percentage + '%';
    valueSpan.textContent = percentage + '%';
}

// Obtener recomendación
async function getRecommendation() {
    if (!currentUserId) {
        showError('Por favor, selecciona un usuario primero');
        return;
    }
    
    try {
        showLoading();
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUserId
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        currentRecommendation = data;
        displayRecommendation(data);
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error obteniendo recomendación: ' + error.message);
    }
}

function displayRecommendation(rec) {
    document.getElementById('recommendationResult').style.display = 'block';
    document.getElementById('artistName').textContent = rec.artist_name;
    document.getElementById('artistId').textContent = rec.artist_id;
    document.getElementById('strategy').textContent = rec.strategy;
    document.getElementById('reason').textContent = rec.reason;
    document.getElementById('confidence').textContent = formatPercentage(rec.confidence);
    
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.width = formatPercentage(rec.confidence);
    
    // Limpiar feedback anterior
    document.getElementById('feedbackResult').innerHTML = '';
    document.getElementById('feedbackResult').className = 'feedback-result';
}

// Enviar feedback
async function submitFeedback(feedbackType) {
    if (!currentRecommendation) {
        showError('No hay recomendación activa');
        return;
    }
    
    try {
        showLoading();
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUserId,
                artist_id: currentRecommendation.artist_id,
                feedback_type: feedbackType
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Mostrar resultado del feedback
        const feedbackResult = document.getElementById('feedbackResult');
        feedbackResult.className = 'feedback-result success';
        feedbackResult.innerHTML = `
            <strong>✅ Feedback registrado</strong><br>
            Recompensa: ${formatNumber(data.reward, 3)}<br>
            Outcome: ${data.outcome}<br>
            ${data.message}
        `;
        
        // Actualizar estadísticas y perfil
        await loadStatistics();
        await loadUserProfile(currentUserId);
        
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error enviando feedback: ' + error.message);
    }
}

// Cargar estadísticas
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Actualizar métricas principales
        document.getElementById('totalUsers').textContent = data.total_users;
        document.getElementById('totalRecommendations').textContent = data.total_recommendations;
        document.getElementById('averageReward').textContent = formatNumber(data.average_reward, 3);
        document.getElementById('activeSessions').textContent = data.active_sessions;
        
        // Actualizar rendimiento por estrategia
        const strategyStatsDiv = document.getElementById('strategyStats');
        strategyStatsDiv.innerHTML = '';
        
        if (data.strategy_performance) {
            Object.entries(data.strategy_performance).forEach(([strategy, stats]) => {
                const strategyItem = document.createElement('div');
                strategyItem.className = 'strategy-item';
                strategyItem.innerHTML = `
                    <div class="strategy-name">${strategy}</div>
                    <div class="strategy-metrics">
                        <span>Usos: ${stats.count}</span>
                        <span>Recompensa: ${formatNumber(stats.avg_reward, 3)}</span>
                        <span>Éxito: ${formatPercentage(stats.success_rate)}</span>
                    </div>
                `;
                strategyStatsDiv.appendChild(strategyItem);
            });
        } else {
            strategyStatsDiv.innerHTML = '<p>No hay datos de estrategias disponibles aún.</p>';
        }
        
    } catch (error) {
        showError('Error cargando estadísticas: ' + error.message);
    }
}

// Cargar perfil del usuario
async function loadUserProfile(userId) {
    try {
        const response = await fetch(`/api/users/${userId}/profile`);
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        const profileContent = document.getElementById('userProfileContent');
        
        if (data.total_interactions === 0) {
            profileContent.innerHTML = `
                <p>Este usuario aún no ha interactuado con el agente.</p>
                <p>Sofisticación del usuario: ${formatPercentage(data.user_sophistication)}</p>
            `;
        } else {
            let historyHTML = '';
            if (data.interaction_history && data.interaction_history.length > 0) {
                historyHTML = '<h4>Últimas interacciones:</h4><ul>';
                data.interaction_history.forEach(interaction => {
                    historyHTML += `
                        <li>
                            ${interaction.artist_name} (${interaction.strategy}) - 
                            Recompensa: ${formatNumber(interaction.reward, 3)} - 
                            ${interaction.outcome}
                        </li>
                    `;
                });
                historyHTML += '</ul>';
            }
            
            profileContent.innerHTML = `
                <div class="profile-stats">
                    <p><strong>Interacciones totales:</strong> ${data.total_interactions}</p>
                    <p><strong>Estrategia preferida:</strong> ${data.preferred_strategy}</p>
                    <p><strong>Confianza del agente:</strong> ${formatPercentage(data.agent_confidence)}</p>
                    <p><strong>Sofisticación:</strong> ${formatPercentage(data.user_sophistication)}</p>
                </div>
                ${historyHTML}
            `;
        }
        
    } catch (error) {
        console.error('Error cargando perfil del usuario:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Cargar usuarios al iniciar
    loadAvailableUsers();
    
    // Cargar estadísticas iniciales
    loadStatistics();
    
    // Botón cargar usuario
    document.getElementById('loadUserBtn').addEventListener('click', function() {
        const userId = document.getElementById('userSelect').value;
        if (userId) {
            loadUserState(parseInt(userId));
        } else {
            showError('Por favor, selecciona un usuario');
        }
    });
    
    // Botón usuario aleatorio
    document.getElementById('randomUserBtn').addEventListener('click', function() {
        if (availableUsers.length > 0) {
            const randomUser = availableUsers[Math.floor(Math.random() * availableUsers.length)];
            document.getElementById('userSelect').value = randomUser;
            loadUserState(randomUser);
        }
    });
    
    // Botón obtener recomendación
    document.getElementById('getRecommendationBtn').addEventListener('click', getRecommendation);
    
    // Botón actualizar estadísticas
    document.getElementById('loadStatsBtn').addEventListener('click', loadStatistics);
});

