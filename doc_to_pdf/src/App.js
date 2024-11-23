import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [file, setFile] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [password, setPassword] = useState("");

  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
    setMetadata(null); // Reset metadata and PDF URL on new upload
    setPdfUrl(null);
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("password", password); // Optional password input

    try {
      const uploadResponse = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Metadata response from backend
      setMetadata(uploadResponse.data.metadata);

      // PDF URL (backend should return the file URL)
      setPdfUrl(uploadResponse.data.pdf_url);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file!");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Word to PDF Converter</h1>
      <div>
        <label>
          Upload .docx File:
          <input type="file" accept=".docx" onChange={handleFileUpload} />
        </label>
      </div>
      <div>
        <label>
          PDF Password (optional):
          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
      </div>
      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        Convert to PDF
      </button>

      {/* {metadata && (
        <div style={{ marginTop: "20px" }}>
          <h2>File Metadata:</h2>
          <p><strong>Name:</strong> {metadata.name}</p>
          <p><strong>Size:</strong> {metadata.size} bytes</p>
          <p><strong>Uploaded At:</strong> {metadata.uploaded_at}</p>
        </div>
      )} */}

      {pdfUrl && (
        <div style={{ marginTop: "20px" }}>
          <h2>Download PDF:</h2>
          <a href={pdfUrl} target="_blank" rel="noopener noreferrer">
            Download Converted PDF
          </a>
        </div>
      )}
    </div>
  );
};

export default App;
