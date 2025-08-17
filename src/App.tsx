import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const res = await fetch("http://localhost:5000/convert", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Conversion failed");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "converted.zip";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error: " + err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>PDF → JPG Converter</h1>

      <input type="file" accept="application/pdf" onChange={handleFileChange} />

      <button onClick={handleSubmit} disabled={!file || loading}>
        {loading ? "Converting..." : "Convert & Download"}
      </button>

      {file && <p>Selected File: {file.name}</p>}
    </div>
  );
}
