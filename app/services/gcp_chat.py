"""
Enhanced chatbot using Google Gemini AI.
"""
import os
from typing import List, Tuple, Optional
import google.generativeai as genai

from .gcp_config import gcp_config


class GCPChatbot:
    """Enhanced chatbot using Google Gemini AI."""
    
    def __init__(self, embedding_index=None):
        self.embedding_index = embedding_index
        self.gemini_model = None
        self.gcp_config = gcp_config
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gemini model."""
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini chatbot initialized")
        except Exception as e:
            print(f"⚠️  Gemini chatbot initialization failed: {e}")
    
    def answer(self, query: str, doc_id: Optional[str] = None) -> Tuple[str, List[str]]:
        """
        Generate answer using Gemini AI with document context.
        """
        if not self.gemini_model:
            return self._fallback_answer(query, doc_id)
        
        try:
            # Get relevant context from document
            contexts = self._get_document_context(query, doc_id)
            
            # Create enhanced prompt with context
            prompt = self._create_enhanced_prompt(query, contexts)
            
            # Generate response
            response = self.gemini_model.generate_content(prompt)
            answer = response.text.strip()
            
            return answer, contexts
            
        except Exception as e:
            print(f"Gemini chat error: {e}")
            return self._fallback_answer(query, doc_id)
    
    def _get_document_context(self, query: str, doc_id: Optional[str]) -> List[str]:
        """Get relevant document context for the query."""
        if not self.embedding_index:
            return []
        
        try:
            results = self.embedding_index.search(query=query, k=5, doc_id=doc_id)
            return [result[2] for result in results if result[2]]
        except Exception as e:
            print(f"Context retrieval error: {e}")
            return []
    
    def _create_enhanced_prompt(self, query: str, contexts: List[str]) -> str:
        """Create an enhanced prompt with document context."""
        context_text = "\n\n".join(contexts) if contexts else "No specific document context available."
        
        prompt = f"""
        You are a helpful legal assistant specializing in document analysis. 
        A user has asked: "{query}"
        
        Here is the relevant context from their legal document:
        {context_text}
        
        Please provide a clear, helpful answer that:
        1. Directly addresses their question
        2. Uses the document context when relevant
        3. Explains legal concepts in plain language
        4. Highlights any important implications or risks
        5. Suggests follow-up questions if appropriate
        
        If the document context doesn't contain relevant information, 
        provide general guidance while noting the limitation.
        
        Keep your response concise but comprehensive.
        """
        
        return prompt
    
    def _fallback_answer(self, query: str, doc_id: Optional[str]) -> Tuple[str, List[str]]:
        """Fallback to basic chatbot if Gemini is not available."""
        from .rag_chat import RAGChatbot
        basic_chatbot = RAGChatbot(self.embedding_index)
        return basic_chatbot.answer(query, doc_id)
    
    def generate_document_insights(self, doc_id: str) -> str:
        """
        Generate comprehensive document insights using Gemini.
        """
        if not self.gemini_model or not self.embedding_index:
            return "AI insights not available."
        
        try:
            # Get all document clauses
            results = self.embedding_index.search("", k=20, doc_id=doc_id)
            all_clauses = [result[2] for result in results if result[2]]
            
            if not all_clauses:
                return "No document content available for analysis."
            
            document_text = "\n\n".join(all_clauses)
            
            prompt = f"""
            Analyze this legal document and provide comprehensive insights including:
            
            1. Document Overview
               - Type of document
               - Main purpose
               - Key parties involved
            
            2. Critical Terms Analysis
               - Most important clauses
               - Potential risks or concerns
               - Unusual or noteworthy terms
            
            3. Practical Implications
               - What the signer should know
               - Recommended actions
               - Questions to ask before signing
            
            4. Risk Assessment
               - High-risk areas
               - Potential legal issues
               - Financial implications
            
            Document content:
            {document_text[:6000]}  # Limit to avoid token limits
            
            Provide a structured, easy-to-understand analysis.
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"Document insights error: {e}")
            return "Error generating document insights."
    
    def suggest_questions(self, doc_id: str) -> List[str]:
        """
        Suggest relevant questions about the document.
        """
        if not self.gemini_model or not self.embedding_index:
            return [
                "What are the main obligations in this document?",
                "What are the termination conditions?",
                "Are there any penalties or fees?",
                "What happens if I breach the contract?",
                "What are my rights under this agreement?"
            ]
        
        try:
            # Get document content
            results = self.embedding_index.search("", k=10, doc_id=doc_id)
            clauses = [result[2] for result in results if result[2]]
            
            if not clauses:
                return ["What is this document about?"]
            
            document_text = "\n\n".join(clauses)
            
            prompt = f"""
            Based on this legal document, suggest 5-7 important questions 
            that someone should ask before signing or agreeing to it.
            
            Focus on:
            - Key obligations and rights
            - Financial terms
            - Termination conditions
            - Liability and risk
            - Dispute resolution
            
            Document content:
            {document_text[:4000]}
            
            Provide questions in a simple, conversational format.
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            # Parse response into list of questions
            questions = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and ('?' in line or line.startswith('-') or line.startswith('•')):
                    # Clean up the question
                    question = line.lstrip('-• ').strip()
                    if question and len(question) > 10:
                        questions.append(question)
            
            return questions[:7] if questions else [
                "What are the main obligations in this document?",
                "What are the termination conditions?",
                "Are there any penalties or fees?"
            ]
            
        except Exception as e:
            print(f"Question suggestion error: {e}")
            return ["What is this document about?"]
    
    def is_available(self) -> bool:
        """Check if Gemini chatbot is available."""
        return self.gemini_model is not None


# Global chatbot instance
gcp_chatbot = GCPChatbot()
