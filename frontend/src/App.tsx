import React, { useState } from "react";
import { Header } from "./components/Header";
import { Description } from "./components/Description";
import { InputSection } from "./components/InputSection";
import { ResultsSection } from "./components/ResultsSection";
import { Footer } from "./components/Footer";
export function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const handleAnalyze = data => {
    setLoading(true);
    // Simulate API call for sentiment analysis
    setTimeout(() => {
      setResults({
        overall: 0.75,
        breakdown: {
          text: 0.8,
          audio: 0.7,
          video: 0.75
        },
        keywords: ["service", "quality", "speed", "cleanliness", "value"]
      });
      setLoading(false);
    }, 1500);
  };
  return <div className="flex flex-col min-h-screen w-full bg-gray-50">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Description />
        <div id="analyze">
          <InputSection onAnalyze={handleAnalyze} loading={loading} />
          {results && <ResultsSection results={results} />}
        </div>
      </main>
      <Footer />
    </div>;
}