import React from "react";
export function TextInput({
  value,
  onChange
}) {
  return <div>
      <label htmlFor="text-review" className="block text-sm font-medium text-gray-700 mb-2">
        Enter McDonald's review text
      </label>
      <textarea id="text-review" rows={6} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500" placeholder="Type or paste a McDonald's review here..." value={value} onChange={e => onChange(e.target.value)}></textarea>
      <p className="mt-2 text-sm text-gray-500">
        For best results, provide a detailed review about your McDonald's
        experience.
      </p>
    </div>;
}