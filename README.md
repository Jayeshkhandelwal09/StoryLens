# StoryLens 📸✨

**Multi-modal Photo Story Generator with AI Narration**

Transform your photos into captivating stories and poems with the power of AI! StoryLens uses advanced computer vision and natural language processing to analyze your images and create unique, creative narratives with optional audio narration.

![StoryLens Demo](https://img.shields.io/badge/Status-Working-brightgreen) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![React](https://img.shields.io/badge/React-18-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)

## 🌟 Features

- **📷 Photo Upload**: Drag & drop interface for easy image uploads
- **🤖 AI Story Generation**: Creates creative stories and poems from your photos
- **🎵 Audio Narration**: Text-to-speech conversion for sharing your stories
- **🎨 Beautiful UI**: Modern, responsive interface built with React and Tailwind CSS
- **⚡ Fast Processing**: Optimized AI models for quick story generation
- **🔄 Multiple Formats**: Generate both stories and poems from the same image

## 🌟 ScreenShots
<img width="1470" alt="Screenshot 2025-06-04 at 8 08 27 AM" src="https://github.com/user-attachments/assets/005ded78-d354-4737-b326-49ec802e32fd" />
<img width="1470" alt="Screenshot 2025-06-04 at 8 08 43 AM" src="https://github.com/user-attachments/assets/d28dd1ae-9a0f-4b13-9411-d2c069cb3fb1" />
<img width="1470" alt="Screenshot 2025-06-04 at 8 08 54 AM" src="https://github.com/user-attachments/assets/fe2774c4-1193-459b-b920-fdd01fd9df00" />



## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **BLIP** - Image captioning and understanding (Salesforce/blip-image-captioning-base)
- **Kosmos-2** - Fallback vision-language model (Microsoft/kosmos-2-patch14-224)
- **XTTS-v2** - Text-to-speech with Tacotron2-DDC fallback
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face model library

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Hot Toast** - Beautiful notifications
- **Lucide React** - Modern icon library

## 📋 Prerequisites

- **Python 3.11** (Required for TTS compatibility)
- **Node.js 16+** and npm
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd StoryLens
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Set Python version to 3.11 (using pyenv)
pyenv local 3.11.9

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install
```

### 4. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage

1. **Upload a Photo**: Drag and drop any image file (JPG, PNG, etc.) into the upload area
2. **Generate Story**: The AI will automatically analyze your image and create a creative story
3. **Switch to Poem**: Click the "Generate Poem" button for a poetic interpretation
4. **Add Audio**: Click "Generate Audio Narration" to create a voice version of your story
5. **Share**: Enjoy and share your AI-generated stories!

## 🎯 API Endpoints

### Upload & Story Generation
- `POST /api/upload` - Upload image and generate story
- `GET /uploads/images/{filename}` - Serve uploaded images

### Audio Generation
- `POST /api/audio/generate` - Generate audio from text
- `GET /api/audio/{filename}` - Serve audio files

### Health & Info
- `GET /` - API information
- `GET /health` - Health check with model status

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the backend directory:

```env
# AI Models
KOSMOS_MODEL_PATH=microsoft/kosmos-2-patch14-224
XTTS_MODEL_PATH=tts_models/multilingual/multi-dataset/xtts_v2

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true

# File Settings
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760  # 10MB

# AI Settings
DEVICE=auto  # auto, cpu, cuda, mps
MAX_STORY_LENGTH=200
AUDIO_SAMPLE_RATE=22050
AUDIO_FORMAT=wav

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## 🧠 AI Models Used

### Image Understanding
1. **BLIP (Primary)**: Salesforce/blip-image-captioning-base
   - Better image understanding and captioning
   - More accurate scene description

2. **Kosmos-2 (Fallback)**: Microsoft/kosmos-2-patch14-224
   - Vision-language model for image analysis
   - Grounding and object detection capabilities

### Text-to-Speech
1. **XTTS-v2 (Primary)**: Multilingual text-to-speech
   - High-quality voice synthesis
   - Multiple language support

2. **Tacotron2-DDC (Fallback)**: English TTS model
   - Reliable speech generation
   - Good quality for English text

### Creative Generation
- **Template-based System**: Uses image descriptions to generate creative stories and poems
- **Multiple Templates**: Various story and poem templates for diversity
- **Contextual Adaptation**: Adapts content based on image analysis

## 📁 Project Structure

```
StoryLens/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration
│   │   ├── services/      # AI services
│   │   └── main.py        # FastAPI app
│   ├── uploads/           # File storage
│   ├── requirements.txt   # Python dependencies
│   └── venv/             # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx        # Main app
│   ├── public/           # Static files
│   └── package.json      # Node dependencies
└── README.md             # This file
```

## 🐛 Troubleshooting

### Common Issues

**1. Python Version Error**
```bash
# Make sure you're using Python 3.11
python --version
pyenv install 3.11.9
pyenv local 3.11.9
```

**2. TTS Model Loading Issues**
- The app will fallback to Tacotron2-DDC if XTTS-v2 fails
- Check logs for model loading status

**3. Frontend Build Errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**4. Port Already in Use**
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Performance Tips

- **GPU Acceleration**: Set `DEVICE=cuda` if you have a compatible GPU
- **Memory Usage**: Models will download on first run (~2-3GB total)
- **Image Size**: Larger images may take longer to process

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the amazing Transformers library
- **Salesforce** for the BLIP model
- **Microsoft** for the Kosmos-2 model
- **Coqui AI** for the TTS models
- **FastAPI** and **React** communities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Look at existing [Issues](../../issues)
3. Create a new issue with detailed information

---

**Made with ❤️ and AI** - Transform your photos into stories! 
