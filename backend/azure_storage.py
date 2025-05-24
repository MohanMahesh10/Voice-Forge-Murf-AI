from azure.storage.blob import BlobServiceClient
import os
import uuid
from pathlib import Path
import logging

def get_blob_service_client():
    """Get Azure Blob Service Client"""
    account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("STORAGE_ACCOUNT_KEY")
    
    if not account_name or not account_key:
        logging.warning("Azure Storage credentials not found in environment variables")
        return None
        
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    return BlobServiceClient.from_connection_string(connection_string)

def upload_file(file_path, container_name):
    """Upload a file to Azure Storage and return the URL"""
    blob_service_client = get_blob_service_client()
    
    if not blob_service_client:
        logging.warning("Could not initialize Azure Blob Service Client")
        return None
    
    # Get file name from path
    file_name = Path(file_path).name
    
    try:
        # Get container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Upload to Azure Storage
        blob_client = container_client.get_blob_client(file_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        return blob_client.url
    except Exception as e:
        logging.error(f"Error uploading to Azure Storage: {str(e)}")
        return None

def download_file(blob_url, local_path):
    """Download a file from Azure Storage"""
    blob_service_client = get_blob_service_client()
    
    if not blob_service_client:
        return False
    
    try:
        # Extract container name and blob name from URL
        # URL format: https://{account}.blob.core.windows.net/{container}/{blob}
        url_parts = blob_url.replace("https://", "").split("/")
        container_name = url_parts[1]
        blob_name = "/".join(url_parts[2:])
        
        # Get blob client
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        
        # Download blob
        with open(local_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        
        return True
    except Exception as e:
        logging.error(f"Error downloading from Azure Storage: {str(e)}")
        return False
