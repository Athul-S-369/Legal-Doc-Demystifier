from typing import List, Tuple, Optional
from .embeddings import EmbeddingIndex
import re


class RAGChatbot:
	def __init__(self, embedding_index: EmbeddingIndex):
		self.embedding_index = embedding_index

	def _generate_answer(self, query: str, contexts: List[str]) -> str:
		if not contexts:
			return "I couldn't find a specific clause matching your question. Try rephrasing or asking about a named section."
		bulleted = '\n'.join(f"- {c[:400]}{'…' if len(c)>400 else ''}" for c in contexts)
		plain = self._plain_language_rewrite(query, contexts)
		guidance = "If this doesn't answer your question, try asking about a specific clause title or include key terms (e.g., 'termination notice period')."
		return f"Relevant clauses:\n{bulleted}\n\nPlain-English answer: {plain}\n\n{guidance}"

	def _plain_language_rewrite(self, query: str, contexts: List[str]) -> str:
		# Heuristic rewrite: look for obligations, rights, time limits, amounts
		text = ' '.join(contexts)
		obligation = 'requires' if re.search(r"\b(shall|must|required|obligated)\b", text, re.I) else 'may allow'
		time_match = re.search(r"within\s+(\d+\s+(days?|business days?|months?))", text, re.I)
		amount_match = re.search(r"\$\s?([0-9,.]+)|([0-9,.]+)\s?(USD|dollars?)", text, re.I)
		time_str = time_match.group(0) if time_match else 'no specific timeline'
		amount_str = amount_match.group(0) if amount_match else 'no specific amount'
		subject_hint = 'party obligations' if re.search(r"party|parties|seller|buyer|licensor|licensee", text, re.I) else 'terms'
		return f"it {obligation} {subject_hint}. I can see {time_str} and {amount_str}."

	def answer(self, query: str, doc_id: Optional[str]) -> Tuple[str, List[str]]:
		results = self.embedding_index.search(query=query, k=3, doc_id=doc_id)  # Reduced from 5 to 3
		contexts = [r[2] for r in results]
		answer = self._generate_answer(query, contexts)
		return answer, contexts


