from flask import Blueprint, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
import os

from .services.ocr import extract_text_from_file
from .services.segment import segment_clauses
from .services.summarize import summarize_text
from .services.risk import analyze_risks
from .services.embeddings import EmbeddingIndex
from .services.rag_chat import RAGChatbot
from .services.storage import encrypt_file_inplace, decrypt_file, delete_document_files


bp = Blueprint('main', __name__)

# Singletons for in-process use
embedding_index = EmbeddingIndex(index_dir=Path('models/faiss_index'))
chatbot = RAGChatbot(embedding_index=embedding_index)


@bp.get('/')
def index():
	return render_template('index.html')


@bp.post('/upload')
def upload():
	if 'document' not in request.files:
		return redirect(url_for('main.index'))
	file = request.files['document']
	if file.filename == '':
		return redirect(url_for('main.index'))

	filename = secure_filename(file.filename)
	uid = uuid.uuid4().hex
	stored_name = f"{uid}_{filename}"
	upload_dir = Path('data/uploads')
	upload_dir.mkdir(parents=True, exist_ok=True)
	file_path = upload_dir / stored_name
	file.save(str(file_path))
	# Encrypt uploaded file at rest
	encrypt_file_inplace(file_path)

	# Decrypt to temp for OCR/text extraction, preserve original extension
	plaintext = decrypt_file(file_path)
	tmp_path = file_path.with_name(f"{file_path.stem}_dec{file_path.suffix}")
	tmp_path.write_bytes(plaintext)
	text = extract_text_from_file(str(tmp_path))
	try:
		tmp_path.unlink()
	except Exception:
		pass
	clauses = segment_clauses(text)
	summary = summarize_text(text)
	risks = analyze_risks(clauses)

	# Index clauses for retrieval
	embedding_index.add_document(doc_id=uid, clauses=clauses)

	processed_dir = Path('data/processed')
	processed_dir.mkdir(parents=True, exist_ok=True)
	(processed_dir / f'{uid}_summary.bin').write_bytes(summary.encode('utf-8'))
	encrypt_file_inplace(processed_dir / f'{uid}_summary.bin')
	(processed_dir / f'{uid}_clauses.bin').write_bytes('\n\n'.join(clauses).encode('utf-8'))
	encrypt_file_inplace(processed_dir / f'{uid}_clauses.bin')

	return render_template('dashboard.html', doc_id=uid, summary=summary, risks=risks, clauses=clauses)


@bp.post('/chat')
def chat():
	data = request.get_json(force=True)
	query = data.get('query', '')
	doc_id = data.get('doc_id')
	answer, citations = chatbot.answer(query=query, doc_id=doc_id)
	return jsonify({
		'answer': answer,
		'citations': citations,
	})


@bp.get('/export/summary/<doc_id>')
def export_summary(doc_id: str):
	path = Path('data/processed') / f'{doc_id}_summary.bin'
	if not path.exists():
		return redirect(url_for('main.index'))
	data = decrypt_file(path)
	tmp = Path('data/processed') / f'{doc_id}_summary.txt'
	tmp.write_bytes(data)
	resp = send_file(str(tmp), as_attachment=True, download_name='summary.txt')
	try:
		tmp.unlink()
	except Exception:
		pass
	return resp


@bp.get('/export/clauses/<doc_id>')
def export_clauses(doc_id: str):
	path = Path('data/processed') / f'{doc_id}_clauses.bin'
	if not path.exists():
		return redirect(url_for('main.index'))
	data = decrypt_file(path)
	tmp = Path('data/processed') / f'{doc_id}_clauses.txt'
	tmp.write_bytes(data)
	resp = send_file(str(tmp), as_attachment=True, download_name='clauses.txt')
	try:
		tmp.unlink()
	except Exception:
		pass
	return resp


@bp.post('/delete/<doc_id>')
def delete_doc(doc_id: str):
	delete_document_files(doc_id)
	return redirect(url_for('main.index'))


@bp.post('/process_text')
def process_text():
	text = request.form.get('raw_text', '').strip()
	if not text:
		return redirect(url_for('main.index'))
	uid = uuid.uuid4().hex
	clauses = segment_clauses(text)
	summary = summarize_text(text)
	risks = analyze_risks(clauses)
	# index for chat
	embedding_index.add_document(doc_id=uid, clauses=clauses)
	return render_template('dashboard.html', doc_id=uid, summary=summary, risks=risks, clauses=clauses)


