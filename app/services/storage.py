from pathlib import Path
from typing import Optional


def delete_document_files(doc_id: str) -> None:
	base = Path('data/processed')
	uploads = Path('data/uploads')
	for p in [
		uploads / f'{doc_id}.bin',
		base / f'{doc_id}_summary.bin',
		base / f'{doc_id}_clauses.bin',
		base / f'{doc_id}_chat.jsonl',
	]:
		try:
			if p.exists():
				p.unlink()
		except Exception:
			pass


