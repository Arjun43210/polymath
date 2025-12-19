import React, { useState } from "react";

export default function UploadForm({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Choose a PDF first.");
    setStatus("Uploading...");
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: form
      });
      const j = await res.json();
      if (!res.ok) throw new Error(j.detail || "Upload failed");
      setStatus(`Indexed ${j.chunks} chunks`);
      onUploaded(j);
    } catch (err) {
      console.error(err);
      setStatus("Upload failed: " + err.message);
    }
  };

  return (
    <div>
      <h2>Upload textbook (PDF)</h2>
      <form onSubmit={handleUpload}>
        <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Upload & Index</button>
      </form>
      <div>{status}</div>
    </div>
  );
}
