import React from "react";
import { MicIcon, VideoIcon, TrendingUpIcon } from "lucide-react";
export function ResultsSection({
  results
}: {
  results: {
    sentiment: string;
    error?: string;
  } | null;
}) {
  // Helper function to get sentiment color and icon
  const getSentimentColor = (sentiment: string) => {
    switch(sentiment.toLowerCase()) {
      case 'positive': return 'bg-green-500';
      case 'neutral': return 'bg-yellow-500';
      case 'negative': return 'bg-red-500';
      case 'error': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  if (!results) return null;

  return <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
    <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
      <TrendingUpIcon className="h-5 w-5 mr-2 text-red-600" />
      Analysis Results
    </h2>
    
    {results.error ? (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-700">{results.error}</p>
      </div>
    ) : (
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Sentiment</h3>
        <div className="flex items-center">
          <div className={`h-12 w-12 rounded-full ${getSentimentColor(results.sentiment)} 
            flex items-center justify-center text-white mr-4`}>
            {results.sentiment.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-medium text-gray-900">
              {results.sentiment.charAt(0).toUpperCase() + results.sentiment.slice(1)}
            </p>
          </div>
        </div>
      </div>
    )}
  </section>;
}