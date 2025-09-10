from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
import json
import re
from collections import Counter


class EmbeddingIndex:
	def __init__(self, index_dir: Path):
		self.index_dir = Path(index_dir)
		self.index_dir.mkdir(parents=True, exist_ok=True)
		self.docid_to_offsets_path = self.index_dir / 'doc_offsets.json'
		self.docid_to_offsets = {}
		self._load()

	def _load(self) -> None:
		if self.docid_to_offsets_path.exists():
			self.docid_to_offsets = json.loads(self.docid_to_offsets_path.read_text(encoding='utf-8'))

	def _save(self) -> None:
		self.docid_to_offsets_path.write_text(json.dumps(self.docid_to_offsets), encoding='utf-8')

	def _simple_similarity(self, text1: str, text2: str) -> float:
		"""Simple word-based similarity without heavy ML models"""
		words1 = set(re.findall(r'\w+', text1.lower()))
		words2 = set(re.findall(r'\w+', text2.lower()))
		if not words1 or not words2:
			return 0.0
		intersection = len(words1 & words2)
		union = len(words1 | words2)
		return intersection / union if union > 0 else 0.0

	def add_document(self, doc_id: str, clauses: List[str]) -> None:
		self.docid_to_offsets[doc_id] = {'clauses': clauses}
		self._save()

	def search(self, query: str, k: int = 3, doc_id: Optional[str] = None) -> List[Tuple[int, float, str]]:
		results: List[Tuple[int, float, str]] = []
		
		if doc_id is None:
			# Search across all documents
			for did, meta in self.docid_to_offsets.items():
				clauses = meta['clauses']
				for i, clause in enumerate(clauses):
					score = self._simple_similarity(query, clause)
					if score > 0.1:  # Threshold for relevance
						results.append((i, score, clause))
		else:
			# Search within specific document
			meta = self.docid_to_offsets.get(doc_id)
			if not meta:
				return []
			clauses = meta['clauses']
			for i, clause in enumerate(clauses):
				score = self._simple_similarity(query, clause)
				if score > 0.1:  # Threshold for relevance
					results.append((i, score, clause))
		
		# Sort by score and return top k
		results.sort(key=lambda x: x[1], reverse=True)
		return results[:k]


