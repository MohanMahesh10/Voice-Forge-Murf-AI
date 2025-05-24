from cloudinary import config, uploader, api
import os
from pathlib import Path
import logging

class CloudinaryStorage:
    """Cloudinary storage integration for Voice Forge"""
    
    def __init__(self):
        # Configure Cloudinary with environment variables
        config(
            cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
            api_key=os.environ.get("CLOUDINARY_API_KEY"),
            api_secret=os.environ.get("CLOUDINARY_API_SECRET")
        )
        
    def upload_file(self, file_path, folder="uploads"):
        """Upload a file to Cloudinary and return the URL"""
        try:
            # Get file name from path
            file_name = Path(file_path).name
            
            # Upload to Cloudinary
            result = uploader.upload(
                file_path,
                resource_type="auto",
                folder=f"voice-forge/{folder}",
                public_id=file_name.split('.')[0]  # Use filename without extension as public_id
            )
            
            return result["secure_url"]
        except Exception as e:
            logging.error(f"Error uploading to Cloudinary: {str(e)}")
            return None
    
    def download_file(self, url, local_path):
        """Download a file from Cloudinary"""
        try:
            # Extract public ID from URL
            # URL format: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{folder}/{public_id}.{extension}
            parts = url.split('/')
            folder_and_id = parts[-2] + '/' + parts[-1].split('.')[0]
            
            # Download the file
            with open(local_path, 'wb') as f:
                f.write(api.resource(folder_and_id)["bytes"])
            
            return True
        except Exception as e:
            logging.error(f"Error downloading from Cloudinary: {str(e)}")
            return False
