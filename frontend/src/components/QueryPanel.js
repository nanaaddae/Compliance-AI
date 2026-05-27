import { useState } from 'react';
import { queryPolicies } from '../services/api';

export default function QueryPanel() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await queryPolicies(question);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-1">Ask a Compliance Question</h2>
      <p className="text-sm text-gray-500 mb-4">Get answers based strictly on uploaded policy documents.</p>

      <form onSubmit={handleQuery} className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Can I work remotely from another country?"
          className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      <button
  type="submit"
  disabled={loading}
  className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition flex items-center gap-2"
>
  {loading ? (
    <>
      <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
      </svg>
      Asking...
    </>
  ) : 'Ask'}
</button>
      </form>

{loading && (
  <div className="mt-4 flex items-center gap-2 text-sm text-gray-500">
    <svg className="animate-spin h-4 w-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
    </svg>
    Searching policy documents and generating answer...
  </div>
)}


      {error && (
        <div className="mt-4 bg-red-50 text-red-600 p-3 rounded text-sm">{error}</div>
      )}

      {result && (
        <div className="mt-4 space-y-4">
          <div className="bg-blue-50 border border-blue-100 rounded p-4">
            <p className="text-sm font-medium text-blue-800 mb-1">Answer</p>
            <p className="text-sm text-gray-700 whitespace-pre-wrap">{result.answer}</p>
          </div>


        </div>
      )}
    </div>
  );
}