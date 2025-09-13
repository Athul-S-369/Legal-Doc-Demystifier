"""
Google Cloud Storage service for document management.
"""
import os
from pathlib import Path
from typing import Optional, List
import uuid
from datetime import datetime

from .gcp_config import gcp_config


class GCPStorageService:
    """Google Cloud Storage service for document storage."""
    
    def __init__(self, bucket_name: Optional[str] = None):
        self.gcp_config = gcp_config
        self.bucket_name = bucket_name or os.getenv('GCS_BUCKET_NAME')
        self.storage_client = gcp_config.get_storage_client()
        self.bucket = None
        self._initialize_bucket()
    
    def _initialize_bucket(self):
        """Initialize Cloud Storage bucket."""
        if not self.storage_client or not self.bucket_name:
            print("⚠️  Cloud Storage not configured")
            return
        
        try:
            self.bucket = self.storage_client.bucket(self.bucket_name)
            # Test bucket access
            self.bucket.exists()
            print(f"✅ Cloud Storage bucket '{self.bucket_name}' initialized")
        except Exception as e:
            print(f"⚠️  Cloud Storage bucket error: {e}")
            self.bucket = None
    
    def upload_document(self, file_path: str, doc_id: str, file_type: str = "document") -> Optional[str]:
        """
        Upload document to Cloud Storage.
        Returns the GCS path if successful, None otherwise.
        """
        if not self.bucket:
            return None
        
        try:
            # Create GCS path
            gcs_path = f"documents/{doc_id}/{file_type}_{doc_id}"
            
            # Upload file
            blob = self.bucket.blob(gcs_path)
            blob.upload_from_filename(file_path)
            
            # Set metadata
            blob.metadata = {
                'doc_id': doc_id,
                'file_type': file_type,
                'upload_time': datetime.utcnow().isoformat(),
                'original_filename': Path(file_path).name
            }
            blob.patch()
            
            print(f"✅ Document uploaded to GCS: {gcs_path}")
            return gcs_path
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None
    
    def upload_text_content(self, content: str, doc_id: str, content_type: str = "text") -> Optional[str]:
        """
        Upload text content to Cloud Storage.
        """
        if not self.bucket:
            return None
        
        try:
            gcs_path = f"documents/{doc_id}/{content_type}_{doc_id}.txt"
            
            blob = self.bucket.blob(gcs_path)
            blob.upload_from_string(content, content_type='text/plain')
            
            blob.metadata = {
                'doc_id': doc_id,
                'content_type': content_type,
                'upload_time': datetime.utcnow().isoformat()
            }
            blob.patch()
            
            return gcs_path
            
        except Exception as e:
            print(f"❌ Text upload error: {e}")
            return None
    
    def download_document(self, gcs_path: str, local_path: str) -> bool:
        """
        Download document from Cloud Storage.
        """
        if not self.bucket:
            return False
        
        try:
            blob = self.bucket.blob(gcs_path)
            blob.download_to_filename(local_path)
            return True
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False
    
    def get_document_url(self, gcs_path: str, expiration_hours: int = 24) -> Optional[str]:
        """
        Generate signed URL for document access.
        """
        if not self.bucket:
            return None
        
        try:
            blob = self.bucket.blob(gcs_path)
            url = blob.generate_signed_url(
                expiration=datetime.utcnow().timestamp() + (expiration_hours * 3600),
                method='GET'
            )
            return url
        except Exception as e:
            print(f"❌ URL generation error: {e}")
            return None
    
    def list_documents(self, doc_id: Optional[str] = None) -> List[dict]:
        """
        List documents in storage.
        """
        if not self.bucket:
            return []
        
        try:
            prefix = f"documents/{doc_id}/" if doc_id else "documents/"
            blobs = self.bucket.list_blobs(prefix=prefix)
            
            documents = []
            for blob in blobs:
                doc_info = {
                    'name': blob.name,
                    'size': blob.size,
                    'created': blob.time_created,
                    'updated': blob.updated,
                    'metadata': blob.metadata or {}
                }
                documents.append(doc_info)
            
            return documents
        except Exception as e:
            print(f"❌ List error: {e}")
            return []
    
    def delete_document(self, gcs_path: str) -> bool:
        """
        Delete document from Cloud Storage.
        """
        if not self.bucket:
            return False
        
        try:
            blob = self.bucket.blob(gcs_path)
            blob.delete()
            return True
        except Exception as e:
            print(f"❌ Delete error: {e}")
            return False
    
    def delete_document_folder(self, doc_id: str) -> bool:
        """
        Delete all files for a document.
        """
        if not self.bucket:
            return False
        
        try:
            prefix = f"documents/{doc_id}/"
            blobs = self.bucket.list_blobs(prefix=prefix)
            
            deleted_count = 0
            for blob in blobs:
                blob.delete()
                deleted_count += 1
            
            print(f"✅ Deleted {deleted_count} files for document {doc_id}")
            return True
        except Exception as e:
            print(f"❌ Folder delete error: {e}")
            return False
    
    def get_document_metadata(self, gcs_path: str) -> Optional[dict]:
        """
        Get document metadata.
        """
        if not self.bucket:
            return None
        
        try:
            blob = self.bucket.blob(gcs_path)
            blob.reload()
            
            return {
                'name': blob.name,
                'size': blob.size,
                'created': blob.time_created,
                'updated': blob.updated,
                'content_type': blob.content_type,
                'metadata': blob.metadata or {}
            }
        except Exception as e:
            print(f"❌ Metadata error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Cloud Storage is available."""
        return self.bucket is not None


# Global storage service instance
gcp_storage_service = GCPStorageService()
