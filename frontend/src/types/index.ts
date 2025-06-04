export interface GeneratedStory {
  id: number;
  title: string;
  content: string;
  story_type: 'story' | 'poem';
  image_filename: string;
  image_path: string;
  generation_time: number;
  model_used: string;
  created_at: string;
  audio_filename?: string;
  audio_path?: string;
}

export interface UploadResponse {
  id: number;
  title: string;
  content: string;
  story_type: string;
  image_filename: string;
  image_path: string;
  generation_time: number;
  model_used: string;
  created_at: string;
  message: string;
}

export interface AudioResponse {
  audio_filename: string;
  audio_path: string;
  generation_time: number;
  duration: number;
  model_used: string;
  message: string;
}

export interface ApiError {
  error: string;
  message: string;
  detail?: string;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  kosmos_model_loaded: boolean;
  tts_model_loaded: boolean;
  upload_dir_exists: boolean;
  error?: string;
}

export interface FileStats {
  total_images: number;
  total_audio_files: number;
  total_size_mb: number;
  upload_dir: string;
  message: string;
} 