import React, { useState } from 'react';
import { Volume2, VolumeX, Download, Share2 } from 'lucide-react';
import toast from 'react-hot-toast';
import apiService from '../services/api';
import type { GeneratedStory, AudioResponse } from '../types';
import AudioPlayer from './AudioPlayer';

interface StoryDisplayProps {
  story: GeneratedStory;
}

const StoryDisplay: React.FC<StoryDisplayProps> = ({ story }) => {
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [audioData, setAudioData] = useState<AudioResponse | null>(null);

  const handleGenerateAudio = async () => {
    if (audioData) {
      // Audio already exists, just show success
      toast.success('Audio already available!');
      return;
    }

    setIsGeneratingAudio(true);
    try {
      const audioResponse: AudioResponse = await apiService.generateAudio(story.content);
      setAudioData(audioResponse);
      toast.success('Audio generated successfully!');
    } catch (error: any) {
      console.error('Audio generation error:', error);
      toast.error(error.response?.data?.detail || 'Failed to generate audio');
    } finally {
      setIsGeneratingAudio(false);
    }
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: story.title,
          text: story.content,
          url: window.location.href
        });
      } catch (error) {
        // User cancelled sharing
      }
    } else {
      // Fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(`${story.title}\n\n${story.content}`);
        toast.success('Story copied to clipboard!');
      } catch (error) {
        toast.error('Failed to copy story');
      }
    }
  };

  const handleDownloadAudio = () => {
    if (audioData) {
      apiService.downloadAudio(audioData.audio_filename);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Image */}
      <div className="aspect-video bg-gray-100">
        <img
          src={apiService.getImageUrl(story.image_filename)}
          alt={story.title}
          className="w-full h-full object-cover"
        />
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Header with actions */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h2 className="text-xl font-bold text-gray-900">{story.title}</h2>
            <div className="flex items-center space-x-2 mt-1">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                story.story_type === 'poem' 
                  ? 'bg-purple-100 text-purple-800' 
                  : 'bg-blue-100 text-blue-800'
              }`}>
                {story.story_type === 'poem' ? '🎭 Poem' : '📖 Story'}
              </span>
              <span className="text-xs text-gray-500">
                {new Date(story.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          
          <div className="flex items-center space-x-2 ml-4">
            <button
              onClick={handleShare}
              className="p-2 rounded-full text-gray-400 hover:text-green-600 hover:bg-green-50 transition-colors"
            >
              <Share2 className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Story Content */}
        <div className="mb-6">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {story.content}
          </p>
        </div>

        {/* Audio Section */}
        <div className="border-t pt-4">
          {audioData ? (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Audio Narration</span>
                <button
                  onClick={handleDownloadAudio}
                  className="flex items-center space-x-1 text-sm text-primary-600 hover:text-primary-700"
                >
                  <Download className="w-4 h-4" />
                  <span>Download</span>
                </button>
              </div>
              <AudioPlayer audioUrl={apiService.getAudioUrl(audioData.audio_filename)} />
            </div>
          ) : (
            <button
              onClick={handleGenerateAudio}
              disabled={isGeneratingAudio}
              className={`w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-lg font-medium transition-colors ${
                isGeneratingAudio
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              }`}
            >
              {isGeneratingAudio ? (
                <>
                  <VolumeX className="w-5 h-5 animate-pulse" />
                  <span>Generating Audio...</span>
                </>
              ) : (
                <>
                  <Volume2 className="w-5 h-5" />
                  <span>Generate Audio Narration</span>
                </>
              )}
            </button>
          )}
        </div>

        {/* Metadata */}
        <div className="mt-4 pt-4 border-t text-xs text-gray-500 space-y-1">
          <div>Generated by {story.model_used} in {story.generation_time?.toFixed(2)}s</div>
          {audioData && (
            <div>Audio by {audioData.model_used} in {audioData.generation_time.toFixed(2)}s</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StoryDisplay; 