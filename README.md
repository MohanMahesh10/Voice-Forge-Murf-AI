# 🎙️ Voice Forge
> Transform voices with the power of AI - A modern web application for voice transformation and audio processing.
![Screenshot 2025-05-25 010701](https://github.com/user-attachments/assets/901f9ac4-d2db-4862-9b9b-df1e4b9dc159)



[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Svelte](https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00)](https://svelte.dev/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)

## 🌟 Features

Voice Forge is your go-to platform for voice transformation, offering:

- 🎤 **Real-time Voice Recording** - Record audio directly in your browser
- 📁 **Audio File Upload** - Transform existing audio files
- 🔄 **Voice Transformation Options**:
  - Gender transformation (Male ↔️ Female)
  - Accent modifications
  - Tone and pitch adjustments
- 🎵 **Real-time Preview** - Listen to transformations instantly
- 📥 **Easy Export** - Download transformed audio in various formats
- 📊 **Transformation History** - Track and manage your voice transformations
- 🔒 **Secure Processing** - All data handling follows best security practices

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- A Murf API key (for voice transformation)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/MohanMahesh10/Voice-Forge-Murf-AI.git
   cd Voice_Forge
   ```

2. **Set up environment variables**
   ```bash
   # Create .env file
   echo "MURF_API_KEY=your_api_key_here" > .env
   ```

3. **Launch the application**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - 🌐 Web Interface: [http://localhost:5173](http://localhost:5173)
   - 🔧 API Endpoint: [http://localhost:8000](http://localhost:8000)
   - 📚 API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🏗️ Architecture

Voice Forge is built with a modern, scalable architecture:

### Backend (FastAPI)

- **Core**: Python 3.9+ with FastAPI framework
- **Audio Processing**: 
  - pydub for audio manipulation
  - NumPy for signal processing
  - Custom pitch-shifting algorithms
- **Storage**: Azure Blob Storage for audio files
- **Security**: Azure Key Vault for secrets management

### Frontend (Svelte)

- **Framework**: SvelteKit for optimal performance
- **Styling**: TailwindCSS for responsive design
- **Audio Visualization**: WaveSurfer.js
- **State Management**: Built-in Svelte stores
- **Notifications**: Svelte French Toast

### DevOps

- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Cloud**: Azure Container Apps
- **Monitoring**: Azure Application Insights

## 📡 API Endpoints

```typescript
// Available endpoints
GET  /api/voices     // List available voice profiles
POST /api/transform  // Transform audio with selected profile
GET  /api/history    // Get transformation history
```

## 📂 Project Structure

```
Voice_Forge/
├── 🔧 backend/               # FastAPI service
│   ├── main.py              # Core application logic
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container config
├── 🎨 frontend/             # Svelte application
│   ├── src/                # Source code
│   │   ├── lib/           # Shared components
│   │   └── routes/        # Page components
│   └── Dockerfile         # Frontend container config
└── 🐳 docker-compose.yml    # Container orchestration
```

## 🚀 Deployment

### Azure Deployment

Voice Forge is optimized for Azure deployment:

1. **Automated Deployment**
   ```bash
   # Using provided script
   ./deploy.sh
   ```

2. **Manual Deployment**
   - Follow [Azure Deployment Guide](AZURE_DEPLOYMENT_GUIDE.md)
   - Uses Azure Container Apps for scalability
   - Integrates with Azure Key Vault for secrets

### Custom Deployment

The application can be deployed to any platform supporting Docker:

1. Build the containers:
   ```bash
   docker-compose build
   ```

2. Configure environment variables
3. Launch the application:
   ```bash
   docker-compose up -d
   ```

## 🛠️ Development

### Setting Up Development Environment

1. **Backend Development**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - For the powerful Python web framework
- [Svelte](https://svelte.dev/) - For the reactive frontend framework
- [TailwindCSS](https://tailwindcss.com/) - For the utility-first CSS framework
- [WaveSurfer.js](https://wavesurfer-js.org/) - For audio visualization
- [Murf API](https://murf.ai/) - For voice transformation capabilities

---

<p align="center"> ALL RIGHTS TO MOHAN MAHESH @2025 </p>
