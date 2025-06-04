import React from 'react';
import { Camera, ArrowLeft } from 'lucide-react';

interface LayoutProps {
  children: React.ReactNode;
  currentView: 'upload' | 'story';
  onViewChange: (view: 'upload' | 'story') => void;
  hasStory: boolean;
}

const Layout: React.FC<LayoutProps> = ({ children, currentView, onViewChange, hasStory }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <Camera className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">StoryLens</h1>
                <p className="text-xs text-gray-500">AI Photo Story Generator</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex space-x-1">
              <button
                onClick={() => onViewChange('upload')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  currentView === 'upload'
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Camera className="w-4 h-4 inline mr-2" />
                Create
              </button>
              
              {hasStory && (
                <button
                  onClick={() => onViewChange('story')}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    currentView === 'story'
                      ? 'bg-primary-600 text-white'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <ArrowLeft className="w-4 h-4 inline mr-2" />
                  View Story
                </button>
              )}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-sm text-gray-500">
              Built with ❤️ using React, FastAPI, and cutting-edge AI models
            </p>
            <div className="mt-2 flex items-center justify-center space-x-4 text-xs text-gray-400">
              <span>Microsoft Kosmos-2</span>
              <span>•</span>
              <span>Coqui XTTS-v2</span>
              <span>•</span>
              <span>Tailwind CSS</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout; 