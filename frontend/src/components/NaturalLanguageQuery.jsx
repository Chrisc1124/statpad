import { useState } from 'react';
import { processQuery } from '../services/api';

function NaturalLanguageQuery() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const exampleQueries = [
    "How many points did Stephen Curry score in 2023-24?",
    "Compare Stephen Curry and LeBron James in 2023-24",
    "Compare Stephen Curry and LeBron James last 5 games",
    "Compare Lakers and Warriors in 2023-24",
    "Lakers vs Warriors last 10 games"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await processQuery(query);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process query');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuery(example);
  };

  const formatStat = (value) => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'number') {
      return value.toFixed(1);
    }
    return value;
  };

  const renderResult = () => {
    if (!result) return null;

    const { type, data } = result;

    if (type === 'player_stats' && data.stats) {
      const stats = data.stats;
      return (
        <div className="mt-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">{stats.name} - {stats.season}</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
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
              <div className="text-sm text-gray-600">FG%</div>
              <div className="text-2xl font-bold text-primary-600">{formatStat(stats.field_goal_percentage)}%</div>
            </div>
          </div>
        </div>
      );
    }

    if (type === 'player_comparison' && data.player1 && data.player2) {
      return (
        <div className="mt-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Player Comparison</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-lg font-bold mb-2">{data.player1.name}</h4>
              <div className="space-y-1 text-sm">
                <div>Points: {formatStat(data.player1.points_per_game)}</div>
                <div>Rebounds: {formatStat(data.player1.total_rebounds)}</div>
                <div>Assists: {formatStat(data.player1.assists)}</div>
              </div>
            </div>
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-lg font-bold mb-2">{data.player2.name}</h4>
              <div className="space-y-1 text-sm">
                <div>Points: {formatStat(data.player2.points_per_game)}</div>
                <div>Rebounds: {formatStat(data.player2.total_rebounds)}</div>
                <div>Assists: {formatStat(data.player2.assists)}</div>
              </div>
            </div>
          </div>
        </div>
      );
    }

    if ((type === 'player_comparison_game_logs' || type === 'team_comparison_game_logs') && data.game_logs) {
      return (
        <div className="mt-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Game Logs</h3>
          {data.game_logs.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Matchup</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {data.game_logs.slice(0, 10).map((game, idx) => (
                    <tr key={idx}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(game.game_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {game.away_team_abbrev || game.away_team_name} @ {game.home_team_abbrev || game.home_team_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {game.away_score} - {game.home_score}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-600">No game logs found.</p>
          )}
        </div>
      );
    }

    if (type === 'error') {
      return (
        <div className="mt-6 bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
          {data.message || 'Could not process query. Please try rephrasing.'}
        </div>
      );
    }

    return (
      <div className="mt-6">
        <pre className="bg-gray-50 p-4 rounded overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className="px-4 py-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Natural Language Query</h2>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <form onSubmit={handleSubmit}>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
            Ask a question about NBA stats
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., How many points did Stephen Curry score in 2023-24?"
            rows="4"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 mb-4"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full md:w-auto px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : 'Ask Question'}
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Example Queries</h3>
        <div className="space-y-2">
          {exampleQueries.map((example, idx) => (
            <button
              key={idx}
              onClick={() => handleExampleClick(example)}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 bg-gray-50 rounded hover:bg-gray-100 transition-colors"
            >
              "{example}"
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Query Type: {result.type}</h3>
          <p className="text-sm text-gray-600 mb-4">Original query: "{result.original_query}"</p>
          {renderResult()}
        </div>
      )}
    </div>
  );
}

export default NaturalLanguageQuery;


