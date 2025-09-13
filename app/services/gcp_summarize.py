"""
Enhanced summarization service using Google Vertex AI and Gemini.
"""
import os
from typing import List, Optional
import google.generativeai as genai

# Try to import Vertex AI models, fallback gracefully if not available
try:
    from vertexai.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    GenerativeModel = None
    VERTEX_AI_AVAILABLE = False

try:
    from vertexai.preview.generative_models import GenerativeModel as PreviewGenerativeModel
    PREVIEW_VERTEX_AI_AVAILABLE = True
except ImportError:
    PreviewGenerativeModel = None
    PREVIEW_VERTEX_AI_AVAILABLE = False

from .gcp_config import gcp_config


class GCPSummarizationService:
    """Enhanced summarization using Google Cloud AI services."""
    
    def __init__(self):
        self.gcp_config = gcp_config
        self.gemini_model = None
        self.vertex_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models."""
        try:
            # Initialize Gemini API
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini model initialized")
            
            # Initialize Vertex AI model
            if self.gcp_config.is_gcp_enabled() and VERTEX_AI_AVAILABLE:
                try:
                    self.vertex_model = GenerativeModel('gemini-1.5-flash')
                    print("✅ Vertex AI model initialized")
                except Exception as e:
                    print(f"⚠️  Vertex AI initialization failed: {e}")
            else:
                print("⚠️  Vertex AI not available")
                    
        except Exception as e:
            print(f"⚠️  AI model initialization failed: {e}")
    
    def summarize_with_gemini(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text using Gemini API.
        """
        if not self.gemini_model:
            return self._fallback_summary(text)
        
        try:
            prompt = f"""
            Please provide a clear, concise summary of the following legal document text.
            Focus on the key points, important clauses, and main obligations.
            Keep the summary under {max_length} words and use plain language.
            
            Document text:
            {text[:4000]}  # Limit input to avoid token limits
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Gemini summarization error: {e}")
            return self._fallback_summary(text)
    
    def summarize_with_vertex(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text using Vertex AI.
        """
        if not self.vertex_model:
            return self._fallback_summary(text)
        
        try:
            prompt = f"""
            Analyze this legal document and provide a comprehensive summary that includes:
            1. Document type and purpose
            2. Key parties involved
            3. Main obligations and rights
            4. Important terms and conditions
            5. Potential risks or concerns
            
            Use clear, non-legal language that anyone can understand.
            Keep the summary under {max_length} words.
            
            Document text:
            {text[:4000]}
            """
            
            response = self.vertex_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Vertex AI summarization error: {e}")
            return self._fallback_summary(text)
    
    def analyze_legal_risks(self, text: str) -> List[dict]:
        """
        Analyze legal risks using AI.
        """
        if not self.gemini_model:
            return self._fallback_risk_analysis(text)
        
        try:
            prompt = f"""
            Analyze the following legal document for potential risks and concerns.
            Identify clauses that might be problematic for the signer.
            For each risk, provide:
            1. Risk level (High/Medium/Low)
            2. Brief description
            3. Why it's concerning
            4. Suggested action
            
            Format your response as a structured list.
            
            Document text:
            {text[:4000]}
            """
            
            response = self.gemini_model.generate_content(prompt)
            return self._parse_risk_response(response.text)
            
        except Exception as e:
            print(f"Risk analysis error: {e}")
            return self._fallback_risk_analysis(text)
    
    def extract_key_clauses(self, text: str) -> List[dict]:
        """
        Extract and categorize key legal clauses.
        """
        if not self.gemini_model:
            return self._fallback_clause_extraction(text)
        
        try:
            prompt = f"""
            Extract and categorize the key legal clauses from this document.
            For each clause, provide:
            1. Clause type (e.g., Payment Terms, Termination, Liability, etc.)
            2. Brief description
            3. Key details
            4. Importance level (High/Medium/Low)
            
            Format as a structured list.
            
            Document text:
            {text[:4000]}
            """
            
            response = self.gemini_model.generate_content(prompt)
            return self._parse_clause_response(response.text)
            
        except Exception as e:
            print(f"Clause extraction error: {e}")
            return self._fallback_clause_extraction(text)
    
    def _fallback_summary(self, text: str) -> str:
        """Fallback summarization using basic text processing."""
        from .summarize import summarize_text
        return summarize_text(text)
    
    def _fallback_risk_analysis(self, text: str) -> List[dict]:
        """Fallback risk analysis."""
        from .risk import analyze_risks
        risks = analyze_risks([text])  # Convert to list format
        return [{'risk_level': 'Medium', 'description': r.preview, 'labels': r.labels} for r in risks]
    
    def _fallback_clause_extraction(self, text: str) -> List[dict]:
        """Fallback clause extraction."""
        from .segment import segment_clauses
        clauses = segment_clauses(text)
        return [{'type': 'General', 'description': clause[:100], 'importance': 'Medium'} for clause in clauses[:5]]
    
    def _parse_risk_response(self, response: str) -> List[dict]:
        """Parse AI risk analysis response."""
        # Simple parsing - in production, use more sophisticated parsing
        risks = []
        lines = response.split('\n')
        current_risk = {}
        
        for line in lines:
            line = line.strip()
            if 'risk level' in line.lower() or 'high' in line.lower() or 'medium' in line.lower() or 'low' in line.lower():
                if current_risk:
                    risks.append(current_risk)
                current_risk = {'risk_level': 'Medium', 'description': line, 'labels': []}
            elif line and current_risk:
                current_risk['description'] += ' ' + line
        
        if current_risk:
            risks.append(current_risk)
        
        return risks[:5]  # Limit to top 5 risks
    
    def _parse_clause_response(self, response: str) -> List[dict]:
        """Parse AI clause extraction response."""
        # Simple parsing - in production, use more sophisticated parsing
        clauses = []
        lines = response.split('\n')
        current_clause = {}
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if current_clause:
                    clauses.append(current_clause)
                current_clause = {'type': 'General', 'description': line, 'importance': 'Medium'}
            elif line and current_clause:
                current_clause['description'] += ' ' + line
        
        if current_clause:
            clauses.append(current_clause)
        
        return clauses[:10]  # Limit to top 10 clauses
    
    def is_available(self) -> bool:
        """Check if AI services are available."""
        return self.gemini_model is not None or self.vertex_model is not None


# Global summarization service instance
gcp_summarization_service = GCPSummarizationService()
