"""
Google Cloud Platform configuration and authentication utilities.
"""
import os
from typing import Optional
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage, secretmanager
from google.cloud import aiplatform
from google.cloud import documentai
import google.generativeai as genai


class GCPConfig:
    """Google Cloud Platform configuration manager."""
    
    def __init__(self):
        self.project_id: Optional[str] = None
        self.location: str = "us-central1"
        self.credentials = None
        self._initialize()
    
    def _initialize(self):
        """Initialize GCP configuration."""
        try:
            # Try to get default credentials
            self.credentials, self.project_id = default()
            
            # Set project ID from environment if not found
            if not self.project_id:
                self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            
            # Initialize AI Platform
            if self.project_id:
                aiplatform.init(
                    project=self.project_id,
                    location=self.location,
                    credentials=self.credentials
                )
            
            # Initialize Generative AI
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
            
            print(f"✅ GCP initialized successfully. Project: {self.project_id}")
            
        except DefaultCredentialsError:
            print("⚠️  No GCP credentials found. Running in local mode.")
            self.project_id = None
            self.credentials = None
    
    def get_storage_client(self) -> Optional[storage.Client]:
        """Get Google Cloud Storage client."""
        if not self.project_id or not self.credentials:
            return None
        return storage.Client(project=self.project_id, credentials=self.credentials)
    
    def get_documentai_client(self) -> Optional[documentai.DocumentProcessorServiceClient]:
        """Get Document AI client."""
        if not self.project_id or not self.credentials:
            return None
        return documentai.DocumentProcessorServiceClient(credentials=self.credentials)
    
    def get_secret_manager_client(self) -> Optional[secretmanager.SecretManagerServiceClient]:
        """Get Secret Manager client."""
        if not self.project_id or not self.credentials:
            return None
        return secretmanager.SecretManagerServiceClient(credentials=self.credentials)
    
    def is_gcp_enabled(self) -> bool:
        """Check if GCP services are available."""
        return self.project_id is not None and self.credentials is not None


# Global GCP configuration instance
gcp_config = GCPConfig()
