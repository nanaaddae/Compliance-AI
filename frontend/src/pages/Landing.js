import { useNavigate } from 'react-router-dom';

const features = [
  {
    icon: '📄',
    title: 'Upload Policy Documents',
    description: 'Compliance officers can upload any PDF policy document and make it instantly queryable.',
  },
  {
    icon: '🤖',
    title: 'AI-Powered Answers',
    description: 'Employees ask questions in plain English and get accurate answers drawn strictly from your policies.',
  },
  {
    icon: '🔒',
    title: 'Role-Based Access',
    description: 'Employees, compliance officers, executives, and admins each see exactly what they need.',
  },
  {
    icon: '📋',
    title: 'Full Audit Trail',
    description: 'Every query is logged. Executives can monitor all compliance questions asked across the organization.',
  },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white">
      {/* Navbar */}
      <nav className="px-8 py-5 flex items-center justify-between max-w-6xl mx-auto">
        <span className="text-blue-600 font-bold text-xl">⚖️ ComplianceAI</span>
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/login')}
            className="text-sm text-gray-600 hover:text-blue-600 transition"
          >
            Sign In
          </button>
          <button
            onClick={() => navigate('/register')}
            className="text-sm bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-8 pt-20 pb-16 text-center">
        <div className="inline-block bg-blue-100 text-blue-700 text-xs font-semibold px-3 py-1 rounded-full mb-6 uppercase tracking-wide">
          AI-Powered Compliance
        </div>
        <h1 className="text-5xl font-extrabold text-gray-900 leading-tight mb-6">
          Ask your company policies <br />
          <span className="text-blue-600">anything.</span>
        </h1>
        <p className="text-lg text-gray-500 mb-10 max-w-2xl mx-auto">
          ComplianceAI lets employees ask natural language questions and get instant, accurate answers
          sourced directly from your uploaded policy documents. No more digging through PDFs.
        </p>
        <div className="flex items-center justify-center gap-4">
          <button
            onClick={() => navigate('/register')}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition text-sm"
          >
            Get Started Free
          </button>
          <button
            onClick={() => navigate('/login')}
            className="text-sm text-gray-600 hover:text-blue-600 transition px-4 py-3"
          >
            Sign in →
          </button>
        </div>
      </section>

      {/* Example query */}
      <section className="max-w-2xl mx-auto px-8 pb-20">
        <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
          <p className="text-xs text-gray-400 uppercase font-semibold mb-3">Example</p>
          <div className="bg-gray-50 rounded-lg px-4 py-3 text-sm text-gray-600 mb-4">
            💬 "Can I expense a client dinner that costs $200 per person?"
          </div>
          <div className="bg-blue-50 rounded-lg px-4 py-3 text-sm text-gray-700">
            🤖 <span className="font-medium">ComplianceAI:</span> The maximum allowable spend for client entertainment is $150.00 USD per person including alcohol, tax, and gratuity. A dinner at $200 per person would exceed this limit and would not be reimbursable unless pre-approved by a VP or higher...
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white border-t border-gray-100 py-20">
        <div className="max-w-5xl mx-auto px-8">
          <h2 className="text-3xl font-bold text-gray-800 text-center mb-12">
            Everything your team needs
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((f, i) => (
              <div key={i} className="flex gap-4">
                <div className="text-3xl">{f.icon}</div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-1">{f.title}</h3>
                  <p className="text-sm text-gray-500">{f.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 text-center px-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Ready to get started?</h2>
        <p className="text-gray-500 mb-8 text-sm">Set up takes minutes. No credit card required.</p>
        <button
          onClick={() => navigate('/register')}
          className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition text-sm"
        >
          Create Your Account
        </button>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-100 py-6 text-center text-xs text-gray-400">
        © 2025 ComplianceAI. Built with FastAPI, React, and LLaMA 3.
      </footer>
    </div>
  );
}