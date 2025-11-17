const API_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export async function askQuestion(question: string): Promise<string> {
  const res = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  const data = await res.json();
  return data.answer;
}