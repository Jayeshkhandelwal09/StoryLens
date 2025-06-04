import axios from 'axios';
import type {
  UploadResponse,
  HealthStatus
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for AI operations
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health and status
  async getHealth(): Promise<HealthStatus> {
    const response = await api.get('/health');
    return response.data;
  },

  async getUploadStatus() {
    const response = await api.get('/api/upload/status');
    return response.data;
  },

  // Upload and story generation
  async uploadImage(file: File, storyType: 'story' | 'poem' = 'story'): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('story_type', storyType);

    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Audio generation
  async generateAudio(text: string, voice: string = 'default') {
    const response = await api.post('/api/audio/generate', {
      text,
      voice
    });
    return response.data;
  },

  // Get audio file URL
  getAudioUrl(filename: string): string {
    return `${API_BASE_URL}/api/audio/${filename}`;
  },

  // Delete audio file
  async deleteAudio(filename: string) {
    const response = await api.delete(`/api/audio/${filename}`);
    return response.data;
  },

  // Get TTS status
  async getTTSStatus() {
    const response = await api.get('/api/audio/status/tts');
    return response.data;
  },

  // Get file statistics
  async getFileStats() {
    const response = await api.get('/api/stories/stats/summary');
    return response.data;
  },

  // Utility functions
  getImageUrl(filename: string): string {
    return `${API_BASE_URL}/uploads/images/${filename}`;
  },

  downloadAudio(filename: string) {
    const url = this.getAudioUrl(filename);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
};

export default apiService; 