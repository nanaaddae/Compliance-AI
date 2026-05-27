import { useState, useEffect } from 'react';
import { listUsers, updateUserRole } from '../services/api';
import Layout from '../components/Layout';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const ROLES = ['employee', 'compliance_officer', 'executive', 'admin'];

const roleColors = {
  admin: 'bg-red-100 text-red-700',
  compliance_officer: 'bg-purple-100 text-purple-700',
  executive: 'bg-yellow-100 text-yellow-700',
  employee: 'bg-green-100 text-green-700',
};

export default function Admin() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(null);
  const [success, setSuccess] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.role !== 'admin') {
      navigate('/dashboard');
      return;
    }
    fetchUsers();
  }, [user]);

  const fetchUsers = async () => {
    try {
      const res = await listUsers();
      setUsers(res.data);
    } catch (err) {
      console.error('Failed to fetch users');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    setUpdating(userId);
    setSuccess('');
    try {
      await updateUserRole(userId, newRole);
      setUsers(users.map(u => u.id === userId ? { ...u, role: newRole } : u));
      setSuccess(`Role updated successfully`);
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      console.error('Failed to update role');
    } finally {
      setUpdating(null);
    }
  };

  return (
    <Layout>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Admin Panel</h1>
          <p className="text-sm text-gray-500 mt-1">Manage user roles and access levels</p>
        </div>
        <button
          onClick={() => navigate('/dashboard')}
          className="text-sm text-blue-600 hover:underline"
        >
          ← Back to Dashboard
        </button>
      </div>

      {success && (
        <div className="mb-4 bg-green-50 text-green-700 px-4 py-3 rounded text-sm">
          ✓ {success}
        </div>
      )}

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-100">
          <h2 className="font-semibold text-gray-700">All Users ({users.length})</h2>
        </div>

        {loading ? (
          <div className="p-8 text-center text-gray-400 text-sm">Loading users...</div>
        ) : (
          <div className="divide-y divide-gray-100">
            {users.map((u) => (
              <div key={u.id} className="px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-9 h-9 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-semibold text-sm">
                    {u.full_name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-800">
                      {u.full_name}
                      {u.id === user.id && (
                        <span className="ml-2 text-xs text-gray-400">(you)</span>
                      )}
                    </p>
                    <p className="text-xs text-gray-500">{u.email}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${roleColors[u.role]}`}>
                    {u.role.replace('_', ' ')}
                  </span>
                  {u.id !== user.id && (
                    <select
                      value={u.role}
                      onChange={(e) => handleRoleChange(u.id, e.target.value)}
                      disabled={updating === u.id}
                      className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                      {ROLES.map(role => (
                        <option key={role} value={role}>
                          {role.replace('_', ' ')}
                        </option>
                      ))}
                    </select>
                  )}
                  {updating === u.id && (
                    <span className="text-xs text-gray-400">Updating...</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
}