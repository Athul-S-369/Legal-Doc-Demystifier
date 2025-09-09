from typing import List, Tuple, Optional
from .embeddings import EmbeddingIndex
import re


class RAGChatbot:
	def __init__(self, embedding_index: EmbeddingIndex):
		self.embedding_index = embedding_index

	def _generate_answer(self, query: str, contexts: List[str]) -> str:
		# Simple extractive + synthesis: quote best spans and synthesize plain-English answer
		joined = '\n'.join(f"- {c}" for c in contexts)
		return (
			"Here's what your document says related to your question: "
			+ joined
			+ "\nIn plain English: This means "
			+ self._plain_language_rewrite(query, contexts)
		)

	def _plain_language_rewrite(self, query: str, contexts: List[str]) -> str:
		# Heuristic rewrite: look for obligations, rights, time limits, amounts
		text = ' '.join(contexts)
		obligation = 'requires' if re.search(r"shall|must|required|obligated", text, re.I) else 'may allow'
		time_match = re.search(r"within\s+(\d+\s+(days?|business days?|months?))", text, re.I)
		amount_match = re.search(r"\$\s?([0-9,.]+)|([0-9,.]+)\s?(USD|dollars?)", text, re.I)
		time_str = time_match.group(0) if time_match else 'no specific timeline'
		amount_str = amount_match.group(0) if amount_match else 'no specific amount'
		return f"it {obligation} something related to your question. I can see {time_str} and {amount_str}."

	def answer(self, query: str, doc_id: Optional[str]) -> Tuple[str, List[str]]:
		results = self.embedding_index.search(query=query, k=3, doc_id=doc_id)  # Reduced from 5 to 3
		contexts = [r[2] for r in results]
		answer = self._generate_answer(query, contexts)
		return answer, contexts


