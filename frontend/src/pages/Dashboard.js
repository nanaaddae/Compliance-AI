import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import QueryPanel from '../components/QueryPanel';
import DocumentsPanel from '../components/DocumentsPanel';
import AuditPanel from '../components/AuditPanel';

export default function Dashboard() {
  const { user } = useAuth();

  const canUpload = ['compliance_officer', 'admin'].includes(user?.role);
  const canViewAllLogs = ['executive', 'admin'].includes(user?.role);

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Welcome back, {user?.full_name.split(' ')[0]} 👋
      </h1>

      <div className="space-y-6">
        {/* Everyone sees the query panel */}
        <QueryPanel />

        {/* Only compliance officers and admins see upload */}
        {canUpload && <DocumentsPanel />}

        {/* Executives and admins see all logs, employees see their own */}
        <AuditPanel showAll={canViewAllLogs} />
      </div>
    </Layout>
  );
}