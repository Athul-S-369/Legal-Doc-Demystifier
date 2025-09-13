"""
Enhanced OCR service using Google Document AI and Cloud Vision.
"""
import os
from pathlib import Path
from typing import List, Optional
import io
from PIL import Image

from .gcp_config import gcp_config
from google.cloud import documentai

# Try to import Vision API, fallback gracefully if not available
try:
    from google.cloud import vision
    VISION_API_AVAILABLE = True
except ImportError:
    vision = None
    VISION_API_AVAILABLE = False


class GCPOCRService:
    """Enhanced OCR service using Google Cloud services."""
    
    def __init__(self):
        self.gcp_config = gcp_config
        self.documentai_client = gcp_config.get_documentai_client()
        self.vision_client = None
        if gcp_config.is_gcp_enabled() and VISION_API_AVAILABLE:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
            except Exception as e:
                print(f"⚠️  Vision API client initialization failed: {e}")
                self.vision_client = None
    
    def extract_text_with_documentai(self, file_path: str, processor_id: Optional[str] = None) -> str:
        """
        Extract text using Google Document AI.
        Requires a Document AI processor to be set up.
        """
        if not self.documentai_client or not processor_id:
            return ""
        
        try:
            # Read the file
            with open(file_path, 'rb') as image:
                image_content = image.read()
            
            # Configure the process request
            raw_document = documentai.RawDocument(
                content=image_content,
                mime_type=self._get_mime_type(file_path)
            )
            
            # Create the request
            request = documentai.ProcessRequest(
                name=f"projects/{self.gcp_config.project_id}/locations/{self.gcp_config.location}/processors/{processor_id}",
                raw_document=raw_document
            )
            
            # Process the document
            result = self.documentai_client.process_document(request=request)
            document = result.document
            
            # Extract text
            return document.text
            
        except Exception as e:
            print(f"Document AI error: {e}")
            return ""
    
    def extract_text_with_vision(self, file_path: str) -> str:
        """
        Extract text using Google Cloud Vision API.
        """
        if not self.vision_client:
            return ""
        
        try:
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations
            
            if texts:
                return texts[0].description
            return ""
            
        except Exception as e:
            print(f"Vision API error: {e}")
            return ""
    
    def extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extract text from PIL Image using Vision API.
        """
        if not self.vision_client:
            return ""
        
        try:
            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            image = vision.Image(content=img_byte_arr)
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations
            
            if texts:
                return texts[0].description
            return ""
            
        except Exception as e:
            print(f"Vision API error: {e}")
            return ""
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type based on file extension."""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        mime_types = {
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.tiff': 'image/tiff',
            '.bmp': 'image/bmp',
            '.gif': 'image/gif'
        }
        
        return mime_types.get(suffix, 'application/octet-stream')
    
    def is_available(self) -> bool:
        """Check if GCP OCR services are available."""
        return self.gcp_config.is_gcp_enabled() and VISION_API_AVAILABLE


# Global OCR service instance
gcp_ocr_service = GCPOCRService()
