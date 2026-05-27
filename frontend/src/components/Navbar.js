import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Navbar() {
  const { user, logoutUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  const roleColors = {
    admin: 'bg-red-100 text-red-700',
    compliance_officer: 'bg-purple-100 text-purple-700',
    executive: 'bg-yellow-100 text-yellow-700',
    employee: 'bg-green-100 text-green-700',
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <span className="text-blue-600 font-bold text-lg">⚖️ ComplianceAI</span>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">{user?.full_name}</span>
        <span className={`text-xs px-2 py-1 rounded-full font-medium ${roleColors[user?.role]}`}>
          {user?.role?.replace('_', ' ')}
        </span>

        {user?.role === 'admin' && (
  <button
    onClick={() => navigate('/admin')}
    className="text-sm text-blue-600 hover:text-blue-800 transition"
  >
    Admin Panel
  </button>
)}


        <button
          onClick={handleLogout}
          className="text-sm text-gray-500 hover:text-red-500 transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}