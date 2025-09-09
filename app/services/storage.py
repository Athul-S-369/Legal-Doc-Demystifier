from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
import os


KEY_PATH = Path('models/secret.key')


def _load_or_create_key() -> bytes:
	KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
	if KEY_PATH.exists():
		return KEY_PATH.read_bytes()
	key = Fernet.generate_key()
	KEY_PATH.write_bytes(key)
	return key


_FERNET = Fernet(_load_or_create_key())


def encrypt_bytes(data: bytes) -> bytes:
	return _FERNET.encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
	return _FERNET.decrypt(token)


def encrypt_file_inplace(path: Path) -> None:
	data = path.read_bytes()
	enc = encrypt_bytes(data)
	path.write_bytes(enc)


def decrypt_file(path: Path) -> bytes:
	data = path.read_bytes()
	return decrypt_bytes(data)


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


