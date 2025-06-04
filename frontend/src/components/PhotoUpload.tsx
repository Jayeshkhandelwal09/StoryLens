import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image, Loader2, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import apiService from '../services/api';
import type { UploadResponse } from '../types';

interface PhotoUploadProps {
  onUploadSuccess: (result: UploadResponse) => void;
  onUploadStart: () => void;
  disabled?: boolean;
}

const PhotoUpload: React.FC<PhotoUploadProps> = ({
  onUploadSuccess,
  onUploadStart,
  disabled = false
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [storyType, setStoryType] = useState<'story' | 'poem'>('story');
  const [preview, setPreview] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Create preview
    const previewUrl = URL.createObjectURL(file);
    setPreview(previewUrl);

    setIsUploading(true);
    onUploadStart();

    try {
      const result = await apiService.uploadImage(file, storyType);
      onUploadSuccess(result);
      toast.success('Story generated successfully!');
    } catch (error: any) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload image');
      setPreview(null);
    } finally {
      setIsUploading(false);
    }
  }, [storyType, onUploadSuccess, onUploadStart]);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    disabled: disabled || isUploading
  });

  const clearPreview = () => {
    if (preview) {
      URL.revokeObjectURL(preview);
      setPreview(null);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Story Type Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          What would you like to generate?
        </label>
        <div className="flex space-x-4">
          <button
            type="button"
            onClick={() => setStoryType('story')}
            disabled={isUploading}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              storyType === 'story'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            } ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            📖 Story
          </button>
          <button
            type="button"
            onClick={() => setStoryType('poem')}
            disabled={isUploading}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              storyType === 'poem'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            } ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            🎭 Poem
          </button>
        </div>
      </div>

      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
          transition-all duration-200 ease-in-out
          ${isDragActive 
            ? 'border-primary-400 bg-primary-50' 
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }
          ${(disabled || isUploading) ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        {preview ? (
          <div className="space-y-4">
            <img
              src={preview}
              alt="Preview"
              className="max-w-full max-h-64 mx-auto rounded-lg shadow-md"
            />
            {!isUploading && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  clearPreview();
                }}
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Remove image
              </button>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {isUploading ? (
              <>
                <Loader2 className="w-12 h-12 mx-auto text-primary-600 animate-spin" />
                <div>
                  <p className="text-lg font-medium text-gray-900">
                    Generating your {storyType}...
                  </p>
                  <p className="text-sm text-gray-500">
                    This may take a few moments
                  </p>
                </div>
              </>
            ) : (
              <>
                <div className="flex justify-center">
                  {isDragActive ? (
                    <Upload className="w-12 h-12 text-primary-600" />
                  ) : (
                    <Image className="w-12 h-12 text-gray-400" />
                  )}
                </div>
                <div>
                  <p className="text-lg font-medium text-gray-900">
                    {isDragActive
                      ? 'Drop your image here'
                      : 'Upload an image to generate a ' + storyType
                    }
                  </p>
                  <p className="text-sm text-gray-500">
                    Drag and drop or click to select • JPEG, PNG, WebP • Max 10MB
                  </p>
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* File Rejection Errors */}
      {fileRejections.length > 0 && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-sm font-medium text-red-800">Upload Error</p>
          </div>
          <ul className="mt-2 text-sm text-red-700">
            {fileRejections.map(({ file, errors }) => (
              <li key={file.name}>
                {file.name}: {errors.map(e => e.message).join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Instructions */}
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-600">
          Upload any photo and our AI will create a creative {storyType} inspired by what it sees.
          You can then generate audio narration to bring your story to life!
        </p>
      </div>
    </div>
  );
};

export default PhotoUpload; 