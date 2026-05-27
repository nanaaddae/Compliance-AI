import { useState, useEffect } from 'react';
import { listDocuments, uploadDocument, deleteDocument } from '../services/api';

export default function DocumentsPanel() {
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const fetchDocuments = async () => {
    try {
      const res = await listDocuments();
      setDocuments(res.data.documents);
    } catch (err) {
      console.error('Failed to fetch documents');
    }
  };

  useEffect(() => { fetchDocuments(); }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (description) formData.append('description', description);
      await uploadDocument(formData);
      setFile(null);
      setDescription('');
      fetchDocuments();
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this document?')) return;
    try {
      await deleteDocument(id);
      fetchDocuments();
    } catch (err) {
      console.error('Delete failed');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-1">Policy Documents</h2>
      <p className="text-sm text-gray-500 mb-4">Upload PDF policy documents for the AI to reference.</p>

      <form onSubmit={handleUpload} className="flex flex-col gap-2 mb-6">
        <div className="flex gap-2">
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm"
          />
          <button
            type="submit"
            disabled={uploading || !file}
            className="bg-green-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition"
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optional)"
          className="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </form>

      {error && (
        <div className="mb-4 bg-red-50 text-red-600 p-3 rounded text-sm">{error}</div>
      )}

      {documents.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-4">No documents uploaded yet.</p>
      ) : (
        <div className="space-y-2">
          {documents.map((doc) => (
            <div key={doc.id} className="flex items-center justify-between bg-gray-50 rounded px-3 py-2">
              <div>
                <p className="text-sm font-medium text-gray-700">📄 {doc.original_name}</p>
                {doc.description && <p className="text-xs text-gray-500">{doc.description}</p>}
                <p className="text-xs text-gray-400">{new Date(doc.created_at).toLocaleDateString()}</p>
              </div>
              <button
                onClick={() => handleDelete(doc.id)}
                className="text-xs text-red-500 hover:text-red-700 transition"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}