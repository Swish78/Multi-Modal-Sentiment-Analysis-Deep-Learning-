import React, { useState } from "react";
import { UploadIcon, MicIcon } from "lucide-react";
export function AudioInput({
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
        Upload audio review
      </label>
      <div className="border-2 border-dashed border-gray-300 rounded-md p-6 flex flex-col items-center">
        <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <MicIcon className="h-6 w-6 text-gray-600" />
        </div>
        {fileName ? <p className="text-sm text-gray-700 mb-2">{fileName}</p> : <p className="text-sm text-gray-500 mb-2">
            MP3, WAV, or M4A up to 10MB
          </p>}
        <label className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 cursor-pointer flex items-center">
          <UploadIcon className="h-4 w-4 mr-2" />
          {fileName ? "Change file" : "Select audio file"}
          <input type="file" className="hidden" accept="audio/mp3,audio/wav,audio/m4a" onChange={handleFileChange} />
        </label>
      </div>
      <p className="mt-2 text-sm text-gray-500">
        Upload a recording of your verbal McDonald's review.
      </p>
    </div>;
}