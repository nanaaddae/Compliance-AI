import { useState, useEffect } from 'react';
import { getMyAuditLogs, getAllAuditLogs } from '../services/api';

export default function AuditPanel({ showAll }) {
  const [logs, setLogs] = useState([]);
  const [expanded, setExpanded] = useState(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [keyword, setKeyword] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [activeFilters, setActiveFilters] = useState({});
  const PAGE_SIZE = 10;
  const totalPages = Math.ceil(total / PAGE_SIZE);

  const fetchLogs = async (p, filters) => {
    const fetch = showAll ? getAllAuditLogs : getMyAuditLogs;
    try {
      const res = await fetch(p, filters);
      setLogs(res.data.logs);
      setTotal(res.data.total);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchLogs(page, activeFilters);
  }, [page, activeFilters, showAll]);

  const handleSearch = () => {
    const filters = {};
    if (keyword.trim()) filters.keyword = keyword.trim();
    if (dateFrom) filters.date_from = new Date(dateFrom).toISOString();
    if (dateTo) filters.date_to = new Date(dateTo).toISOString();
    setActiveFilters(filters);
    setPage(1);
  };

  const handleClear = () => {
    setKeyword('');
    setDateFrom('');
    setDateTo('');
    setActiveFilters({});
    setPage(1);
  };

  const hasActiveFilters = Object.keys(activeFilters).length > 0;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-lg font-semibold text-gray-800">
          {showAll ? 'All Query Logs' : 'My Query History'}
        </h2>
        <span className="text-xs text-gray-400">{total} total</span>
      </div>
      <p className="text-sm text-gray-500 mb-4">
        {showAll ? 'Every compliance question asked across the organization.' : 'Your personal query history.'}
      </p>

      {/* Filters */}
      <div className="bg-gray-50 rounded-lg p-4 mb-4 space-y-3">
        <div className="flex gap-2">
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search questions or answers..."
            className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex gap-2 items-center">
          <div className="flex items-center gap-2 flex-1">
            <label className="text-xs text-gray-500 shrink-0">From</label>
            <input
              type="date"
              value={dateFrom}
              onChange={(e) => setDateFrom(e.target.value)}
              className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex items-center gap-2 flex-1">
            <label className="text-xs text-gray-500 shrink-0">To</label>
            <input
              type="date"
              value={dateTo}
              onChange={(e) => setDateTo(e.target.value)}
              className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={handleSearch}
            className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 transition"
          >
            Search
          </button>
          {hasActiveFilters && (
            <button
              onClick={handleClear}
              className="text-sm text-gray-500 hover:text-red-500 transition px-2"
            >
              Clear
            </button>
          )}
        </div>
        {hasActiveFilters && (
          <p className="text-xs text-blue-600">Filters active — showing filtered results</p>
        )}
      </div>

      {logs.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-4">
          {hasActiveFilters ? 'No results match your filters.' : 'No queries yet.'}
        </p>
      ) : (
        <>
          <div className="space-y-2 mb-4">
            {logs.map((log) => (
              <div key={log.id} className="border border-gray-100 rounded overflow-hidden">
                <button
                  onClick={() => setExpanded(expanded === log.id ? null : log.id)}
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 transition text-left"
                >
                  <span className="text-sm font-medium text-gray-700 truncate">{log.question}</span>
                  <span className="text-xs text-gray-400 ml-4 shrink-0">
                    {new Date(log.created_at).toLocaleDateString()}
                  </span>
                </button>
                {expanded === log.id && (
                  <div className="px-4 py-3 bg-white">
                    <p className="text-sm text-gray-700 whitespace-pre-wrap">{log.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-2 border-t border-gray-100">
              <button
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
                className="text-sm text-blue-600 hover:text-blue-800 disabled:text-gray-300 disabled:cursor-not-allowed transition"
              >
                ← Previous
              </button>
              <span className="text-xs text-gray-500">
                Page {page} of {totalPages}
              </span>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page === totalPages}
                className="text-sm text-blue-600 hover:text-blue-800 disabled:text-gray-300 disabled:cursor-not-allowed transition"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}