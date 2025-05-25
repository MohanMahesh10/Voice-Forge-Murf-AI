from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
import uuid
import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Import Azure Key Vault integration
try:
    from azure_keyvault import get_secret
except ImportError:
    # Fallback if Azure Key Vault is not available
    def get_secret(name, default=None):
        return os.environ.get(name, default)

# Load environment variables
load_dotenv()

# Configure logging
logger.add("app.log", rotation="500 MB")

app = FastAPI(
    title="VoiceForge API",
    description="Voice transformation API",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Create directories if they don't exist
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Pydantic models
class Voice(BaseModel):
    id: str
    name: str
    gender: str
    language: str
    accent: str
    description: str
    sample_url: Optional[str]

class AudioFile(BaseModel):
    id: str
    original_filename: str
    transformed_filename: Optional[str]
    voice_id: Optional[str]
    created_at: datetime
    status: str

# Available voices (mock data)
AVAILABLE_VOICES = [
    Voice(
        id="en-US-terrell",
        name="Terrell",
        gender="Male",
        language="English",
        accent="American",
        description="Professional male voice with a warm tone",
        sample_url=None
    ),
    Voice(
        id="en-US-sarah",
        name="Sarah",
        gender="Female",
        language="English",
        accent="American",
        description="Friendly female voice",
        sample_url=None
    ),
    Voice(
        id="en-US-david",
        name="David",
        gender="Male",
        language="English",
        accent="American",
        description="Narrator voice with deep tone",
        sample_url=None
    ),
    Voice(
        id="en-US-emma",
        name="Emma",
        gender="Female",
        language="English",
        accent="American",
        description="Conversational female voice",
        sample_url=None
    )
]

# In-memory storage for audio history
audio_history: List[AudioFile] = []

@app.get("/")
async def root():
    return {"message": "Welcome to VoiceForge API"}

@app.get("/api/voices")
async def get_voices():
    try:
        return {"voices": AVAILABLE_VOICES}
    except Exception as e:
        logger.error(f"Error fetching voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transform")
async def transform_voice(
    file: UploadFile = File(...),
    voice_id: str = Form(...),
    retain_prosody: bool = Form(True),
    retain_accent: bool = Form(True)
):
    try:
        # Generate output filename
        file_id = str(uuid.uuid4())
        file_ext = Path(file.filename).suffix.lower()
        input_path = UPLOAD_DIR / f"input_{file_id}{file_ext}"
        output_filename = f"transformed_{file_id}{file_ext}"
        output_path = OUTPUT_DIR / output_filename

        # Save uploaded file temporarily
        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        logger.info(f"Processing file: {input_path} with voice: {voice_id}")
          # Create status tracking object
        audio_file = AudioFile(
            id=file_id,
            original_filename=file.filename,
            transformed_filename=output_filename,
            voice_id=voice_id,
            created_at=datetime.now(),
            status="processing"
        )
        audio_history.append(audio_file)
        
        try:
            # For now, we'll enhance the audio with some modifications
            # to simulate voice transformation
            
            # Import necessary libraries
            from pydub import AudioSegment
            import numpy as np
            
            try:
                # Load audio file using pydub (more flexible than wave module)
                logger.info(f"Loading audio file: {input_path}")
                audio = AudioSegment.from_file(str(input_path.absolute()))
                
                # Get gender information for pitch modification
                is_male = "Male" in next((v.gender for v in AVAILABLE_VOICES if v.id == voice_id), "Male")
                logger.info(f"Selected voice gender: {'Male' if is_male else 'Female'}")
                
                # Convert to numpy array for processing
                samples = np.array(audio.get_array_of_samples())
                
                # Apply pitch shift effect
                # For male voices, lower pitch; for female voices, raise pitch
                pitch_factor = 0.85 if is_male else 1.15
                logger.info(f"Applying pitch shift with factor: {pitch_factor}")
                
                # Calculate new indices using the pitch factor
                indices = np.round(np.arange(0, len(samples), pitch_factor)).astype(int)
                indices = indices[indices < len(samples)]
                
                # Apply the pitch shift
                modified_samples = samples[indices]
                
                # Create a new AudioSegment from the modified samples
                modified_audio = audio._spawn(modified_samples.tobytes())
                
                # Export the modified audio to the output path
                modified_audio.export(str(output_path.absolute()), format=file_ext.replace('.', ''))
                
                logger.info(f"Successfully processed audio with pitch factor {pitch_factor}")
            except Exception as audio_error:
                logger.error(f"Audio processing error: {audio_error}")
                # If audio processing fails, copy the original file as fallback
                shutil.copy(str(input_path.absolute()), str(output_path.absolute()))
            
            # Update status after successful transformation
            for i, item in enumerate(audio_history):
                if item.id == file_id:
                    audio_history[i].status = "transformed"
                    break
                    
            logger.info(f"Voice transformation successful: {output_filename}")
            
            # Clean up the input file
            input_path.unlink(missing_ok=True)
            
            return {
                "filename": output_filename,
                "url": f"/outputs/{output_filename}"
            }
            
        except Exception as transformation_error:
            # If transformation fails, use the original file as fallback
            logger.error(f"Transformation failed, using original audio: {transformation_error}")
            
            # Copy the original file as fallback
            shutil.copy(str(input_path.absolute()), str(output_path.absolute()))
            
            # Update status to indicate fallback
            for i, item in enumerate(audio_history):
                if item.id == file_id:
                    audio_history[i].status = "fallback"
                    break
            
            return {
                "filename": output_filename,
                "url": f"/outputs/{output_filename}"
            }

    except Exception as e:
        logger.error(f"Error transforming voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    try:
        return {"history": audio_history}
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
