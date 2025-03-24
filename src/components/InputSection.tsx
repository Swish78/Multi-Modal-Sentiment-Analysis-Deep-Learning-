import React, { useState } from "react";
import { TextInput } from "./inputs/TextInput";
import { AudioInput } from "./inputs/AudioInput";
import { VideoInput } from "./inputs/VideoInput";
import { Loader2Icon } from "lucide-react";
export function InputSection({
  onAnalyze,
  loading
}) {
  const [activeTab, setActiveTab] = useState("text");
  const [inputData, setInputData] = useState({
    text: "",
    audio: null,
    video: null
  });
  const handleInputChange = (type, value) => {
    setInputData(prev => ({
      ...prev,
      [type]: value
    }));
  };
  const handleSubmit = e => {
    e.preventDefault();
    onAnalyze(inputData);
  };
  return <section className="bg-white rounded-lg shadow-lg border border-gray-200 mb-12 transform transition-all duration-300 hover:shadow-xl">
      <div className="flex border-b">
        <button className={`px-6 py-4 text-sm font-medium transition-colors ${activeTab === "text" ? "border-b-2 border-red-500 text-red-600 bg-red-50" : "text-gray-500 hover:text-red-600 hover:bg-red-50"}`} onClick={() => setActiveTab("text")}>
          Text Review
        </button>
        <button className={`px-6 py-4 text-sm font-medium transition-colors ${activeTab === "audio" ? "border-b-2 border-red-500 text-red-600 bg-red-50" : "text-gray-500 hover:text-red-600 hover:bg-red-50"}`} onClick={() => setActiveTab("audio")}>
          Audio Review
        </button>
        <button className={`px-6 py-4 text-sm font-medium transition-colors ${activeTab === "video" ? "border-b-2 border-red-500 text-red-600 bg-red-50" : "text-gray-500 hover:text-red-600 hover:bg-red-50"}`} onClick={() => setActiveTab("video")}>
          Video Review
        </button>
      </div>
      <form onSubmit={handleSubmit} className="p-8">
        <div className={activeTab === "text" ? "block" : "hidden"}>
          <TextInput value={inputData.text} onChange={value => handleInputChange("text", value)} />
        </div>
        <div className={activeTab === "audio" ? "block" : "hidden"}>
          <AudioInput onChange={file => handleInputChange("audio", file)} />
        </div>
        <div className={activeTab === "video" ? "block" : "hidden"}>
          <VideoInput onChange={file => handleInputChange("video", file)} />
        </div>
        <div className="mt-8 flex justify-end">
          <button type="submit" disabled={loading} className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-md font-medium flex items-center shadow-md hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed">
            {loading ? <>
                <Loader2Icon className="animate-spin mr-2 h-4 w-4" />
                Analyzing...
              </> : "Analyze Sentiment"}
          </button>
        </div>
      </form>
    </section>;
}