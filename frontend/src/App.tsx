import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import QueryPanel from "./components/QueryPanel";

export default function App() {
  const [uploaded, setUploaded] = useState(false);
  const [lastUploadInfo, setLastUploadInfo] = useState(null);

  return (
    <div className="container">
      <h1>Textbook RAG demo</h1>
      <UploadForm onUploaded={(info) => { setUploaded(true); setLastUploadInfo(info); }} />
      <hr />
      <QueryPanel disabled={!uploaded} lastUploadInfo={lastUploadInfo} />
    </div>
  );
}
