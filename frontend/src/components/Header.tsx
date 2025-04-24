import React from "react";
import { HomeIcon, InfoIcon, PhoneIcon, MessageSquareIcon } from "lucide-react";
export function Header() {
  return <header className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4 border-b border-gray-100">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center mr-3 shadow-lg transform hover:scale-105 transition-transform">
              <div className="text-yellow-400 h-7 w-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                McDonald's Review Analyzer
              </h1>
              <p className="text-sm text-gray-600">
                Multimodal Sentiment Analysis
              </p>
            </div>
          </div>
        </div>
        <nav className="py-3">
          <ul className="flex space-x-8">
            <li>
              <a href="#" className="flex items-center text-gray-700 hover:text-red-600 transition-colors">
                <HomeIcon className="h-4 w-4 mr-2" />
                Home
              </a>
            </li>
            <li>
              <a href="#about" className="flex items-center text-gray-700 hover:text-red-600 transition-colors">
                <InfoIcon className="h-4 w-4 mr-2" />
                About
              </a>
            </li>
            <li>
              <a href="#analyze" className="flex items-center text-gray-700 hover:text-red-600 transition-colors">
                <div className="h-4 w-4 mr-2" />
                Analyze
              </a>
            </li>
            <li>
              <a href="#contact" className="flex items-center text-gray-700 hover:text-red-600 transition-colors">
                <PhoneIcon className="h-4 w-4 mr-2" />
                Contact
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>;
}