import React from "react";
import { MicIcon, VideoIcon, TrendingUpIcon } from "lucide-react";
export function ResultsSection({
  results
}) {
  // Helper function to get sentiment class
  const getSentimentClass = score => {
    if (score > 0.7) return "bg-green-500";
    if (score > 0.4) return "bg-yellow-500";
    return "bg-red-500";
  };
  // Helper function to get sentiment text
  const getSentimentText = score => {
    if (score > 0.7) return "Positive";
    if (score > 0.4) return "Neutral";
    return "Negative";
  };
  return <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
      <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
        <TrendingUpIcon className="h-5 w-5 mr-2 text-red-600" />
        Sentiment Analysis Results
      </h2>
      {/* Overall sentiment */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Overall Sentiment
        </h3>
        <div className="flex items-center">
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div className={`h-4 rounded-full ${getSentimentClass(results.overall)}`} style={{
            width: `${results.overall * 100}%`
          }}></div>
          </div>
          <span className="ml-4 font-medium">
            {getSentimentText(results.overall)}
          </span>
        </div>
      </div>
      {/* Breakdown by modality */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Sentiment by Modality
        </h3>
        <div className="space-y-4">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <div className="h-4 w-4 text-blue-600" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Text</span>
                <span className="text-sm text-gray-600">
                  {Math.round(results.breakdown.text * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className={`h-2 rounded-full ${getSentimentClass(results.breakdown.text)}`} style={{
                width: `${results.breakdown.text * 100}%`
              }}></div>
              </div>
            </div>
          </div>
          <div className="flex items-center">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-3">
              <MicIcon className="h-4 w-4 text-green-600" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Audio</span>
                <span className="text-sm text-gray-600">
                  {Math.round(results.breakdown.audio * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className={`h-2 rounded-full ${getSentimentClass(results.breakdown.audio)}`} style={{
                width: `${results.breakdown.audio * 100}%`
              }}></div>
              </div>
            </div>
          </div>
          <div className="flex items-center">
            <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
              <VideoIcon className="h-4 w-4 text-purple-600" />
            </div>
            <div className="flex-1">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Video</span>
                <span className="text-sm text-gray-600">
                  {Math.round(results.breakdown.video * 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className={`h-2 rounded-full ${getSentimentClass(results.breakdown.video)}`} style={{
                width: `${results.breakdown.video * 100}%`
              }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Key topics */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Key Topics Identified
        </h3>
        <div className="flex flex-wrap gap-2">
          {results.keywords.map((keyword, index) => <span key={index} className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">
              {keyword}
            </span>)}
        </div>
      </div>
    </section>;
}