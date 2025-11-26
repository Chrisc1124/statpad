import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Player Stats
export const getPlayerStats = async (playerName, season) => {
  const response = await api.get(`/players/${encodeURIComponent(playerName)}/seasons/${season}`);
  return response.data;
};

// Player Comparisons
export const comparePlayers = async (player1, player2, season) => {
  const response = await api.get(
    `/compare/players/${encodeURIComponent(player1)}/${encodeURIComponent(player2)}/seasons/${season}`
  );
  return response.data;
};

export const getPlayerGameLogs = async (player1, player2, season = null, lastN = null) => {
  let url;
  if (season) {
    url = `/compare/players/${encodeURIComponent(player1)}/${encodeURIComponent(player2)}/game-logs/seasons/${season}`;
  } else {
    url = `/compare/players/${encodeURIComponent(player1)}/${encodeURIComponent(player2)}/game-logs/all-seasons`;
  }
  
  if (lastN) {
    url += `?last_n=${lastN}`;
  }
  
  const response = await api.get(url);
  return response.data;
};

// Team Comparisons
export const compareTeams = async (team1, team2, season, includeGameLogs = false, lastN = null) => {
  let url = `/compare/teams/${encodeURIComponent(team1)}/${encodeURIComponent(team2)}/seasons/${season}`;
  const params = new URLSearchParams();
  
  if (includeGameLogs) {
    params.append('include_game_logs', 'true');
  }
  if (lastN) {
    params.append('last_n', lastN);
  }
  
  if (params.toString()) {
    url += `?${params.toString()}`;
  }
  
  const response = await api.get(url);
  return response.data;
};

// Natural Language Query
export const processQuery = async (query) => {
  const response = await api.post('/query', { query });
  return response.data;
};

export default api;


