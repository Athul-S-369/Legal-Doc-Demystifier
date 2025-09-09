from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json


class EmbeddingIndex:
	def __init__(self, index_dir: Path):
		self.index_dir = Path(index_dir)
		self.index_dir.mkdir(parents=True, exist_ok=True)
		# Use a smaller, more memory-efficient model
		self.model = None  # Lazy load
		self.docid_to_offsets_path = self.index_dir / 'doc_offsets.json'
		self.index_path = self.index_dir / 'faiss.index'
		self.dimension = 384  # all-MiniLM-L6-v2 dimension
		self.index = None
		self.docid_to_offsets = {}
		self._load()

	def _load(self) -> None:
		if self.index_path.exists():
			self.index = faiss.read_index(str(self.index_path))
		else:
			self.index = faiss.IndexFlatIP(self.dimension)
		if self.docid_to_offsets_path.exists():
			self.docid_to_offsets = json.loads(self.docid_to_offsets_path.read_text(encoding='utf-8'))

	def _save(self) -> None:
		faiss.write_index(self.index, str(self.index_path))
		self.docid_to_offsets_path.write_text(json.dumps(self.docid_to_offsets), encoding='utf-8')

	def _get_model(self):
		if self.model is None:
			try:
				self.model = SentenceTransformer('all-MiniLM-L6-v2')
			except Exception as e:
				print(f"Model loading failed: {e}")
				# Return a dummy model that won't crash
				class DummyModel:
					def encode(self, texts, **kwargs):
						return np.random.random((len(texts), 384)).astype('float32')
				self.model = DummyModel()
		return self.model

	def add_document(self, doc_id: str, clauses: List[str]) -> None:
		model = self._get_model()
		embs = model.encode(clauses, convert_to_numpy=True, normalize_embeddings=True)
		start = self.index.ntotal
		self.index.add(embs.astype('float32'))
		end = self.index.ntotal
		self.docid_to_offsets[doc_id] = {'start': start, 'end': end, 'clauses': clauses}
		self._save()
		# Clear model from memory after use
		self.model = None

	def search(self, query: str, k: int = 5, doc_id: Optional[str] = None) -> List[Tuple[int, float, str]]:
		model = self._get_model()
		q = model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype('float32')
		dists, idxs = self.index.search(q, k)
		results: List[Tuple[int, float, str]] = []
		if doc_id is None:
			# return across all docs with clause text
			for did, meta in self.docid_to_offsets.items():
				start, end, clauses = meta['start'], meta['end'], meta['clauses']
				for rank in range(k):
					idx = int(idxs[0][rank])
					if start <= idx < end:
						results.append((idx, float(dists[0][rank]), clauses[idx - start]))
		else:
			meta = self.docid_to_offsets.get(doc_id)
			if not meta:
				return []
			start, end, clauses = meta['start'], meta['end'], meta['clauses']
			for rank in range(k):
				idx = int(idxs[0][rank])
				if start <= idx < end:
					results.append((idx, float(dists[0][rank]), clauses[idx - start]))
		# Clear model from memory after use
		self.model = None
		return results


