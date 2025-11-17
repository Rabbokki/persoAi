const API_URL = "http://localhost:8000"; // 배포 시 Vercel URL로 변경

export async function askQuestion(question: string): Promise<string> {
  const res = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  const data = await res.json();
  return data.answer;
}