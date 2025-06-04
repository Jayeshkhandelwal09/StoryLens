import React, { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import PhotoUpload from './components/PhotoUpload';
import StoryDisplay from './components/StoryDisplay';
import type { GeneratedStory, UploadResponse } from './types';

type ViewType = 'upload' | 'story';

function App() {
  const [currentView, setCurrentView] = useState<ViewType>('upload');
  const [currentStory, setCurrentStory] = useState<GeneratedStory | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUploadSuccess = (result: UploadResponse) => {
    // Convert UploadResponse to GeneratedStory format
    const newStory: GeneratedStory = {
      id: result.id,
      title: result.title,
      content: result.content,
      story_type: result.story_type as 'story' | 'poem',
      image_filename: result.image_filename,
      image_path: result.image_path,
      generation_time: result.generation_time,
      model_used: result.model_used,
      created_at: result.created_at,
    };

    // Set current story and switch to story view
    setCurrentStory(newStory);
    setCurrentView('story');
  };

  const handleUploadStart = () => {
    setIsUploading(true);
  };

  const handleBackToUpload = () => {
    setCurrentView('upload');
    setCurrentStory(null);
  };

  const renderContent = () => {
    switch (currentView) {
      case 'upload':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Transform Your Photos into Stories
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Upload any photo and watch as our AI creates a unique story or poem 
                inspired by what it sees. Add voice narration to bring your stories to life!
              </p>
            </div>
            
            <PhotoUpload
              onUploadSuccess={handleUploadSuccess}
              onUploadStart={handleUploadStart}
              disabled={isUploading}
            />
          </div>
        );

      case 'story':
        return (
          <div className="max-w-4xl mx-auto">
            <div className="mb-6">
              <button
                onClick={handleBackToUpload}
                className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                <span>Create Another Story</span>
              </button>
            </div>
            
            {currentStory && (
              <StoryDisplay story={currentStory} />
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="App">
      <Layout 
        currentView={currentView} 
        onViewChange={setCurrentView}
        hasStory={currentStory !== null}
      >
        {renderContent()}
      </Layout>
      
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}

export default App;
