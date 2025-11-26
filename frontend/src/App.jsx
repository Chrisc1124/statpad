import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import PlayerStats from './components/PlayerStats';
import HeadToHead from './components/HeadToHead';
import NaturalLanguageQuery from './components/NaturalLanguageQuery';

function Navigation() {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path ? 'bg-primary-600 text-white' : 'text-gray-700 hover:bg-gray-100';
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">🏀 StatPad</h1>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                to="/"
                className={`${isActive('/')} inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium transition-colors`}
              >
                Player Stats
              </Link>
              <Link
                to="/head-to-head"
                className={`${isActive('/head-to-head')} inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium transition-colors`}
              >
                Head-to-Head
              </Link>
              <Link
                to="/query"
                className={`${isActive('/query')} inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium transition-colors`}
              >
                Ask Question
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navigation />
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<PlayerStats />} />
            <Route path="/head-to-head" element={<HeadToHead />} />
            <Route path="/query" element={<NaturalLanguageQuery />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;


