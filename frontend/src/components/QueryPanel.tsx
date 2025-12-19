import React, { useState } from "react";

export default function QueryPanel({ disabled }) {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [retrieved, setRetrieved] = useState([]);

  const ask = async () => {
    if (!q) return;
    setLoading(true);
    setAnswer(null);
    setRetrieved([]);
    try {
      const res = await fetch("http://localhost:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, top_k: 6 })
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.detail || "Query failed");
      setAnswer(j.answer);
      setRetrieved(j.retrieved || []);
    } catch (err) {
      setAnswer("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Ask a question</h2>
      <textarea value={q} onChange={(e) => setQ(e.target.value)} rows={3} cols={70} disabled={disabled} />
      <div>
        <button onClick={ask} disabled={disabled || loading}>Ask</button>
      </div>
      {loading && <div>Thinking…</div>}
      {answer && (
        <div className="answer">
          <h3>Answer</h3>
          <div>{answer}</div>
          <h4>Sources</h4>
          <ol>
            {retrieved.map((r, i) => (
              <li key={i}><strong>p{r.page}</strong> — {r.text.slice(0, 250)}{r.text.length > 250 ? "…" : ""}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
