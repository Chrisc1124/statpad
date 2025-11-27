import { useState } from 'react';
import { comparePlayers, getPlayerGameLogs } from '../services/api';

function HeadToHead() {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [season, setSeason] = useState('2023-24');
  const [lastN, setLastN] = useState('');
  const [comparison, setComparison] = useState(null);
  const [gameLogs, setGameLogs] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('season'); // 'season' or 'game-logs'

  const handleSeasonComparison = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setComparison(null);
    setGameLogs(null);

    try {
      const data = await comparePlayers(player1, player2, season);
      if (data && data.player1 && data.player2) {
        setComparison(data);
        setViewMode('season');
        setError(null);
      } else {
        setError('One or both players not found for this season');
      }
    } catch (err) {
      console.error('Error fetching player comparison:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to fetch player comparison');
      setComparison(null);
    } finally {
      setLoading(false);
    }
  };

  const handleGameLogs = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setComparison(null);
    setGameLogs(null);

    try {
      const data = await getPlayerGameLogs(player1, player2, season, lastN ? parseInt(lastN) : null);
      if (data && data.game_logs) {
        setGameLogs(data);
        setViewMode('game-logs');
        setError(null);
      } else {
        setError('No game logs found for these players');
      }
    } catch (err) {
      console.error('Error fetching game logs:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to fetch game logs');
      setGameLogs(null);
    } finally {
      setLoading(false);
    }
  };

  const formatStat = (value) => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'number') {
      return value.toFixed(1);
    }
    return value;
  };

  return (
    <div className="px-4 py-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Head-to-Head Comparison</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <form onSubmit={viewMode === 'season' ? handleSeasonComparison : handleGameLogs}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label htmlFor="player1" className="block text-sm font-medium text-gray-700 mb-2">
                Player 1
              </label>
              <input
                type="text"
                id="player1"
                value={player1}
                onChange={(e) => setPlayer1(e.target.value)}
                placeholder="e.g., Stephen Curry"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                required
              />
            </div>
            <div>
              <label htmlFor="player2" className="block text-sm font-medium text-gray-700 mb-2">
                Player 2
              </label>
              <input
                type="text"
                id="player2"
                value={player2}
                onChange={(e) => setPlayer2(e.target.value)}
                placeholder="e.g., LeBron James"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label htmlFor="season" className="block text-sm font-medium text-gray-700 mb-2">
                Season
              </label>
              <input
                type="text"
                id="season"
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                placeholder="e.g., 2023-24"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                required
              />
            </div>
            <div>
              <label htmlFor="lastN" className="block text-sm font-medium text-gray-700 mb-2">
                Last N Games (optional, for game logs)
              </label>
              <input
                type="number"
                id="lastN"
                value={lastN}
                onChange={(e) => setLastN(e.target.value)}
                placeholder="e.g., 5"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setViewMode('season')}
              className={`px-6 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                viewMode === 'season'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Season Stats
            </button>
            <button
              type="button"
              onClick={() => setViewMode('game-logs')}
              className={`px-6 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
                viewMode === 'game-logs'
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Game Logs
            </button>
            <button
              type="submit"
              disabled={loading}
              className="ml-auto px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Loading...' : 'Compare'}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {comparison && viewMode === 'season' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">
            {player1} vs {player2} - {season}
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {comparison.player1 && (
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="text-xl font-bold text-gray-900 mb-4">{comparison.player1.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Points/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player1.points_per_game)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Rebounds/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player1.total_rebounds)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Assists/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player1.assists)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">FG%:</span>
                    <span className="font-bold">{formatStat(comparison.player1.field_goal_percentage)}%</span>
                  </div>
                </div>
              </div>
            )}
            {comparison.player2 && (
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="text-xl font-bold text-gray-900 mb-4">{comparison.player2.name}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Points/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player2.points_per_game)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Rebounds/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player2.total_rebounds)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Assists/Game:</span>
                    <span className="font-bold">{formatStat(comparison.player2.assists)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">FG%:</span>
                    <span className="font-bold">{formatStat(comparison.player2.field_goal_percentage)}%</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {gameLogs && viewMode === 'game-logs' && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">
            Game Logs: {player1} vs {player2}
          </h3>
          
          {gameLogs.game_logs && gameLogs.game_logs.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Matchup</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{player1}</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">{player2}</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {gameLogs.game_logs.map((game, idx) => (
                    <tr key={idx}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(game.game_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {game.away_team_abbrev} @ {game.home_team_abbrev}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {game.player1_points} PTS, {game.player1_rebounds} REB, {game.player1_assists} AST
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {game.player2_points} PTS, {game.player2_rebounds} REB, {game.player2_assists} AST
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-600">No game logs found for these players.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default HeadToHead;


