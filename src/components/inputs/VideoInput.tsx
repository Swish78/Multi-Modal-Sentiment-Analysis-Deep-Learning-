import React, { useState } from "react";
import { UploadIcon, VideoIcon } from "lucide-react";
export function VideoInput({
  onChange
}) {
  const [fileName, setFileName] = useState("");
  const handleFileChange = e => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      onChange(file);
    }
  };
  return <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Upload video review
      </label>
      <div className="border-2 border-dashed border-gray-300 rounded-md p-6 flex flex-col items-center">
        <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <VideoIcon className="h-6 w-6 text-gray-600" />
        </div>
        {fileName ? <p className="text-sm text-gray-700 mb-2">{fileName}</p> : <p className="text-sm text-gray-500 mb-2">
            MP4, MOV, or AVI up to 100MB
          </p>}
        <label className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 cursor-pointer flex items-center">
          <UploadIcon className="h-4 w-4 mr-2" />
          {fileName ? "Change file" : "Select video file"}
          <input type="file" className="hidden" accept="video/mp4,video/mov,video/avi" onChange={handleFileChange} />
        </label>
      </div>
      <p className="mt-2 text-sm text-gray-500">
        Upload a video of your McDonald's review for comprehensive analysis.
      </p>
    </div>;
}