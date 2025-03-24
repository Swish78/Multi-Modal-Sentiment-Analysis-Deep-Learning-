import React from "react";
import { PhoneIcon, MailIcon, MapPinIcon, FacebookIcon, TwitterIcon, InstagramIcon } from "lucide-react";
export function Footer() {
  return <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Contact Information */}
          <div>
            <h3 className="text-xl font-semibold mb-4 text-yellow-400">
              Contact Us
            </h3>
            <ul className="space-y-3">
              <li className="flex items-center">
                <PhoneIcon className="h-5 w-5 mr-3 text-red-500" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center">
                <MailIcon className="h-5 w-5 mr-3 text-red-500" />
                <span>support@mcsentiment.com</span>
              </li>
              <li className="flex items-center">
                <MapPinIcon className="h-5 w-5 mr-3 text-red-500" />
                <span>110 McDonald's Plaza, Chicago, IL</span>
              </li>
            </ul>
          </div>
          {/* Quick Links */}
          <div>
            <h3 className="text-xl font-semibold mb-4 text-yellow-400">
              Quick Links
            </h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="hover:text-red-500 transition-colors">
                  Home
                </a>
              </li>
              <li>
                <a href="#about" className="hover:text-red-500 transition-colors">
                  About
                </a>
              </li>
              <li>
                <a href="#analyze" className="hover:text-red-500 transition-colors">
                  Start Analysis
                </a>
              </li>
              <li>
                <a href="#contact" className="hover:text-red-500 transition-colors">
                  Contact
                </a>
              </li>
            </ul>
          </div>
          {/* Social Media */}
          <div>
            <h3 className="text-xl font-semibold mb-4 text-yellow-400">
              Follow Us
            </h3>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-red-500 transition-colors">
                <FacebookIcon className="h-6 w-6" />
              </a>
              <a href="#" className="hover:text-red-500 transition-colors">
                <TwitterIcon className="h-6 w-6" />
              </a>
              <a href="#" className="hover:text-red-500 transition-colors">
                <InstagramIcon className="h-6 w-6" />
              </a>
            </div>
            <p className="mt-4 text-sm text-gray-400">
              Stay connected with us on social media for updates and news.
            </p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>
            © 2023 McDonald's Sentiment Analysis Tool. All rights reserved.
          </p>
        </div>
      </div>
    </footer>;
}