from pathlib import Path
from typing import List, Tuple, Optional, Dict
import json
import re
import math


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

	def _tokenize(self, text: str) -> List[str]:
		return re.findall(r"[a-z0-9]+", text.lower())

	def _build_idf(self, clauses: List[str]) -> Dict[str, float]:
		n = len(clauses)
		df: Dict[str, int] = {}
		for c in clauses:
			tokens = set(self._tokenize(c))
			for t in tokens:
				df[t] = df.get(t, 0) + 1
		idf: Dict[str, float] = {}
		for t, d in df.items():
			idf[t] = math.log((n + 1) / (d + 0.5)) + 1.0
		return idf

	def _bm25_like(self, query: str, clause: str, idf: Dict[str, float]) -> float:
		q_tokens = self._tokenize(query)
		c_tokens = self._tokenize(clause)
		if not q_tokens or not c_tokens:
			return 0.0
		c_len = len(c_tokens)
		avg_len = 50.0
		k1 = 1.2
		b = 0.75
		term_counts: Dict[str, int] = {}
		for t in c_tokens:
			term_counts[t] = term_counts.get(t, 0) + 1
		score = 0.0
		seen = set()
		for t in q_tokens:
			if t in seen:
				continue
			seen.add(t)
			ft = term_counts.get(t, 0)
			if ft == 0:
				continue
			idf_t = idf.get(t, 0.5)
			numer = ft * (k1 + 1)
			denom = ft + k1 * (1 - b + b * (c_len / avg_len))
			score += idf_t * (numer / denom)
		# Phrase boost for exact bigrams
		bigrams_q = set(zip(q_tokens, q_tokens[1:]))
		bigrams_c = set(zip(c_tokens, c_tokens[1:]))
		if bigrams_q & bigrams_c:
			score *= 1.2
		return score

	def add_document(self, doc_id: str, clauses: List[str]) -> None:
		idf = self._build_idf(clauses)
		self.docid_to_offsets[doc_id] = {'clauses': clauses, 'idf': idf}
		self._save()

	def search(self, query: str, k: int = 5, doc_id: Optional[str] = None) -> List[Tuple[int, float, str]]:
		results: List[Tuple[int, float, str]] = []
		threshold = 0.01
		
		if doc_id is None:
			# Search across all documents
			for did, meta in self.docid_to_offsets.items():
				clauses = meta['clauses']
				idf = meta.get('idf', self._build_idf(clauses))
				for i, clause in enumerate(clauses):
					score = self._bm25_like(query, clause, idf)
					if score >= threshold:  # Threshold for relevance
						results.append((i, score, clause))
		else:
			# Search within specific document
			meta = self.docid_to_offsets.get(doc_id)
			if not meta:
				return []
			clauses = meta['clauses']
			idf = meta.get('idf', self._build_idf(clauses))
			for i, clause in enumerate(clauses):
				score = self._bm25_like(query, clause, idf)
				if score >= threshold:  # Threshold for relevance
					results.append((i, score, clause))
		
		# Sort by score and return top k
		results.sort(key=lambda x: x[1], reverse=True)
		top = results[:k]
		# Fallback: if nothing matched, return top-k longest clauses as context
		if not top and 'clauses' in locals():
			longest = sorted([(i, len(c), c) for i, c in enumerate(clauses)], key=lambda x: x[1], reverse=True)[:k]
			return [(i, 0.0, c) for i, _, c in longest]
		return top


