import React from "react";
import { LineChartIcon, MicIcon, VideoIcon } from "lucide-react";
export function Description() {
  return <section className="mb-12 mt-6" id="about">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Multimodal Sentiment Analysis
        </h2>
        <p className="text-gray-700 max-w-2xl mx-auto">
          Analyze McDonald's customer feedback across different formats to gain
          comprehensive insights. Our advanced AI system processes text, audio,
          and video reviews to detect sentiment, identify key themes, and
          provide actionable intelligence.
        </p>
      </div>
      <div className="grid md:grid-cols-3 gap-6 mt-8">
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-shadow transform hover:-translate-y-1 duration-300">
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
            <div className="h-6 w-6 text-blue-600" />
          </div>
          <h3 className="font-semibold text-lg mb-2">Text Analysis</h3>
          <p className="text-gray-600">
            Process written reviews to identify sentiment and extract key topics
            and concerns.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-shadow transform hover:-translate-y-1 duration-300">
          <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <MicIcon className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="font-semibold text-lg mb-2">Audio Analysis</h3>
          <p className="text-gray-600">
            Analyze tone, emotion, and content from audio reviews for deeper
            customer insights.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 hover:shadow-lg transition-shadow transform hover:-translate-y-1 duration-300">
          <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
            <VideoIcon className="h-6 w-6 text-purple-600" />
          </div>
          <h3 className="font-semibold text-lg mb-2">Video Analysis</h3>
          <p className="text-gray-600">
            Extract visual cues, facial expressions, and verbal feedback from
            video reviews.
          </p>
        </div>
      </div>
    </section>;
}