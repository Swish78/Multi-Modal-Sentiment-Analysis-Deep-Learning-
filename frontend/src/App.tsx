import React, { useState } from "react";
import { Header } from "./components/Header";
import { Description } from "./components/Description";
import { InputSection } from "./components/InputSection";
import { ResultsSection } from "./components/ResultsSection";
import { Footer } from "./components/Footer";

export function App() {
  const [results, setResults] = useState<{sentiment: string; error?: string} | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (data) => {
    setLoading(true);
    try {
      let response;
      if (data.text) {
        response = await fetch("http://127.0.0.1:8000/sentiment/text", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json"
          },
          credentials: 'include',
          body: JSON.stringify({ text: data.text }),
        });
      } else {
        const formData = new FormData();
        const file = data.audio || data.video;
        if (!file) {
          console.error('No file selected');
          setLoading(false);
          return;
        }
        formData.append('file', file);
        response = await fetch("http://localhost:8000/sentiment/media", {
          method: "POST",
          body: formData,
        });
      }
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const json = await response.json();
      if (json.error) {
        setResults({ sentiment: 'error', error: json.error });
      } else {
        setResults({ sentiment: json.sentiment });  
      }
    } catch (err) {
      console.error('Analysis failed:', err);
      setResults({ sentiment: 'error', error: 'Failed to analyze content. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-gray-50">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Description />
        <div id="analyze">
          <InputSection onAnalyze={handleAnalyze} loading={loading} />
          {results && <ResultsSection results={results} />}
        </div>
      </main>
      <Footer />
    </div>
  );
}