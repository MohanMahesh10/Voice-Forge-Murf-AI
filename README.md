# Voice Forge

A web-based voice transformation application that allows you to modify audio recordings with different voice effects.

## Features

- Record audio directly from your browser
- Upload audio files for transformation
- Transform voices with different voice profiles:
  - Male to female voice conversion
  - Female to male voice conversion
  - Various accent transformations
- Listen to transformed audio in real-time
- Download transformed audio files
- View history of voice transformations

## Architecture

Voice Forge is built with a modern tech stack:

- **Backend**: FastAPI (Python)
- **Frontend**: Svelte with TailwindCSS
- **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Running Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Voice_Forge.git
   cd Voice_Forge
   ```

2. Create a `.env` file in the root directory with your MURF API key:
   ```
   MURF_API_KEY=your_api_key_here
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up
   ```

4. Access the application:
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

- `GET /api/voices` - Get list of available voice profiles
- `POST /api/transform` - Transform an audio file with a selected voice profile
- `GET /api/history` - Get history of voice transformations

## Project Structure

```
Voice_Forge/
├── backend/               # FastAPI Python backend
│   ├── main.py           # Main application file
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Backend Docker configuration
│   ├── uploads/          # Directory for uploaded audio files
│   └── outputs/          # Directory for transformed audio files
├── frontend/              # Svelte frontend
│   ├── src/              # Source code
│   │   ├── lib/          # Libraries and components
│   │   └── routes/       # Application routes
│   ├── Dockerfile        # Frontend Docker configuration
│   └── package.json      # Node.js dependencies
└── docker-compose.yml     # Docker Compose configuration
```

## Deployment

The application can be deployed to Azure using Container Apps:

1. Push Docker images to Azure Container Registry
2. Deploy backend and frontend as separate Container Apps
3. Set up Azure Storage for file uploads and outputs

## Technologies Used

- **Backend**:
  - FastAPI
  - pydub (audio processing)
  - NumPy (signal processing)
  - Python 3.9+

- **Frontend**:
  - Svelte
  - TailwindCSS
  - TypeScript
  - Vite

- **DevOps**:
  - Docker
  - Docker Compose
  - GitHub

## License

[MIT](LICENSE)

## Acknowledgements

- FastAPI for the efficient Python web framework
- Svelte for the reactive frontend framework
- TailwindCSS for the utility-first CSS framework
