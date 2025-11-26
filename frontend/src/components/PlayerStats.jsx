import { useState } from 'react';
import { getPlayerStats } from '../services/api';

function PlayerStats() {
  const [playerName, setPlayerName] = useState('');
  const [season, setSeason] = useState('2023-24');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setStats(null);

    try {
      const data = await getPlayerStats(playerName, season);
      setStats(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch player stats');
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
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Player Statistics</h2>
      
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="playerName" className="block text-sm font-medium text-gray-700 mb-2">
              Player Name
            </label>
            <input
              type="text"
              id="playerName"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              placeholder="e.g., Stephen Curry"
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              required
            />
          </div>
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
        </div>
        <button
          type="submit"
          disabled={loading}
          className="mt-4 w-full md:w-auto px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Loading...' : 'Get Stats'}
        </button>
      </form>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {stats && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            {stats.name} - {stats.season}
          </h3>
          {stats.team_name && (
            <p className="text-gray-600 mb-6">{stats.team_name} ({stats.team_abbrev})</p>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Points/Game</div>
              <div className="text-2xl font-bold text-primary-600">{formatStat(stats.points_per_game)}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Rebounds/Game</div>
              <div className="text-2xl font-bold text-primary-600">{formatStat(stats.total_rebounds)}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Assists/Game</div>
              <div className="text-2xl font-bold text-primary-600">{formatStat(stats.assists)}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-600">Games Played</div>
              <div className="text-2xl font-bold text-primary-600">{stats.games_played || 0}</div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Stat
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Value
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Field Goal %</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.field_goal_percentage)}%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">3-Point %</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.three_point_percentage)}%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Free Throw %</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.free_throw_percentage)}%</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Steals/Game</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.steals)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Blocks/Game</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.blocks)}</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Turnovers/Game</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatStat(stats.turnovers)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default PlayerStats;


