import { useState } from "react";

export default function App() {
  // 1. Input + single‐response states
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  // 2. History state: an array of { question, answer }
  const [history, setHistory] = useState([]);

  // 3. Preloaded SIS questions (if you still want them)
  const PRELOADED_QUESTIONS = [
    "How do I schedule a new surgical case?",
    "Show me today's OR schedule for Dr. Smith.",
    "How do I add a patient to the system?",
    "What is the process to cancel an appointment?",
    "How can I update a surgeon’s availability?",
  ];

  // 4. When the user submits (or clicks a preloaded button),
  //    send to the backend and then append to history.
  const handleSubmit = async (e, preloadedText) => {
    e.preventDefault();

    // If they clicked a preloaded question, use that; otherwise use `input`.
    const textToSend = preloadedText !== undefined ? preloadedText : input.trim();
    if (!textToSend) return;

    setLoading(true);
    setResponse(""); // clear any previous single-response while loading

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textToSend }),
      });
      const data = await res.json();

      // 4a. Update the single `response` (for the box below)
      setResponse(data.response);

      // 4b. Append to history
      setHistory((prev) => [
        ...prev,
        { question: textToSend, answer: data.response },
      ]);
    } catch {
      setResponse("Error: Unable to reach server.");
      setHistory((prev) => [
        ...prev,
        { question: textToSend, answer: "Error: Unable to reach server." },
      ]);
    }

    setLoading(false);
    setInput(""); // clear input field after sending
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      <h1 className="text-3xl font-semibold text-blue-600 mb-6">
        SIS AI Assistant
      </h1>

      {/* 5. Preloaded questions (optional) */}
      <div className="mb-4 flex flex-wrap gap-2">
        {PRELOADED_QUESTIONS.map((q) => (
          <button
            key={q}
            onClick={(e) => handleSubmit(e, q)}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-3 py-1 rounded-full text-sm"
          >
            {q}
          </button>
        ))}
      </div>

      {/* 6. The input + “Ask” button form */}
      <form
        onSubmit={(e) => handleSubmit(e)}
        className="w-full max-w-xl flex gap-2 mb-4"
      >
        <input
          type="text"
          placeholder="Ask a surgical question…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 border border-gray-300 px-4 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Thinking…" : "Ask"}
        </button>
      </form>

      {/* 7. History panel: show all previous Q&A */}
      <div className="w-full max-w-xl space-y-4 mb-6">
        {history.map((item, i) => (
          <div key={i}>
            <p className="font-medium text-blue-600">User: {item.question}</p>
            <pre className="bg-gray-100 p-2 rounded text-gray-800">
              AI: {item.answer}
            </pre>
          </div>
        ))}
      </div>

      {/* 8. Single-response box (latest response) */}
      <div className="w-full max-w-xl bg-white border border-gray-200 rounded-lg shadow-sm p-4">
        {response ? (
          <pre className="whitespace-pre-wrap text-gray-800">{response}</pre>
        ) : (
          <p className="text-gray-500">Your answer will appear here.</p>
        )}
      </div>
    </div>
  );
}


