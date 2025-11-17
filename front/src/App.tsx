import { useState } from 'react';
import { askQuestion } from './api';

function App() {
  const [messages, setMessages] = useState<{ role: 'user' | 'bot'; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuestion = input;
    setMessages(prev => [...prev, { role: 'user', content: userQuestion }]);
    setInput('');
    setLoading(true);

    try {
      const answer = await askQuestion(userQuestion);
      setMessages(prev => [...prev, { role: 'bot', content: answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: '서버 연결 오류가 발생했습니다.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-3xl shadow-2xl overflow-hidden">
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6 text-center">
          <h1 className="text-3xl font-bold">Perso.ai 지식 챗봇</h1>
          <p className="text-purple-100 mt-2">할루시네이션 없이 정확한 답변만 제공합니다</p>
        </div>

        <div className="h-96 overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-10">
              <p className="text-lg">Perso.ai에 대해 궁금한 점을 물어보세요!</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-5 py-3 rounded-2xl shadow-md ${
                msg.role === 'user'
                  ? 'bg-purple-600 text-white'   
                  : 'bg-white text-gray-800 border border-gray-200'  
              }`}
            >
              {msg.content}
            </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white px-5 py-3 rounded-2xl border border-gray-200">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="p-6 bg-white border-t">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="질문을 입력하세요..."
              className="flex-1 px-5 py-4 border border-gray-300 rounded-full focus:outline-none focus:ring-4 focus:ring-purple-300 text-lg"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-full hover:from-purple-700 hover:to-pink-700 transition shadow-lg disabled:opacity-50"
            >
              전송
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;