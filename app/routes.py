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
# Storage encryption disabled for lightweight deploy; use plain files


bp = Blueprint('main', __name__)

# Singletons for in-process use - lazy initialization
embedding_index = None
chatbot = None

def get_embedding_index():
	global embedding_index
	if embedding_index is None:
		embedding_index = EmbeddingIndex(index_dir=Path('models/faiss_index'))
	return embedding_index

def get_chatbot():
	global chatbot
	if chatbot is None:
		chatbot = RAGChatbot(embedding_index=get_embedding_index())
	return chatbot


@bp.get('/')
def index():
	return render_template('index.html')


@bp.post('/upload')
def upload():
	try:
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
		
		# For now, skip encryption to avoid potential issues
		text = extract_text_from_file(str(file_path))
		
		clauses = segment_clauses(text)
		summary = summarize_text(text)
		risks = analyze_risks(clauses)

		# Index clauses for retrieval
		get_embedding_index().add_document(doc_id=uid, clauses=clauses)

		processed_dir = Path('data/processed')
		processed_dir.mkdir(parents=True, exist_ok=True)
		(processed_dir / f'{uid}_summary.bin').write_bytes(summary.encode('utf-8'))
		(processed_dir / f'{uid}_clauses.bin').write_bytes('\n\n'.join(clauses).encode('utf-8'))

		return render_template('dashboard.html', doc_id=uid, summary=summary, risks=risks, clauses=clauses)
	except Exception as e:
		return f"Error processing document: {str(e)}", 500


@bp.post('/chat')
def chat():
	try:
		data = request.get_json(force=True)
		query = data.get('query', '')
		doc_id = data.get('doc_id')
		answer, citations = get_chatbot().answer(query=query, doc_id=doc_id)
		return jsonify({
			'answer': answer,
			'citations': citations,
		})
	except Exception as e:
		return jsonify({
			'answer': f"Error processing chat: {str(e)}",
			'citations': [],
		}), 500


@bp.get('/export/summary/<doc_id>')
def export_summary(doc_id: str):
	try:
		path = Path('data/processed') / f'{doc_id}_summary.bin'
		if not path.exists():
			return redirect(url_for('main.index'))
		data = path.read_bytes()
		tmp = Path('data/processed') / f'{doc_id}_summary.txt'
		tmp.write_bytes(data)
		resp = send_file(str(tmp), as_attachment=True, download_name='summary.txt')
		try:
			tmp.unlink()
		except Exception:
			pass
		return resp
	except Exception as e:
		return f"Error exporting summary: {str(e)}", 500


@bp.get('/export/clauses/<doc_id>')
def export_clauses(doc_id: str):
	try:
		path = Path('data/processed') / f'{doc_id}_clauses.bin'
		if not path.exists():
			return redirect(url_for('main.index'))
		data = path.read_bytes()
		tmp = Path('data/processed') / f'{doc_id}_clauses.txt'
		tmp.write_bytes(data)
		resp = send_file(str(tmp), as_attachment=True, download_name='clauses.txt')
		try:
			tmp.unlink()
		except Exception:
			pass
		return resp
	except Exception as e:
		return f"Error exporting clauses: {str(e)}", 500


@bp.post('/delete/<doc_id>')
def delete_doc(doc_id: str):
	# Remove processed artifacts if present
	processed_dir = Path('data/processed')
	for suffix in ['_summary.bin', '_clauses.bin', '_summary.txt', '_clauses.txt']:
		p = processed_dir / f'{doc_id}{suffix}'
		try:
			if p.exists():
				p.unlink()
		except Exception:
			pass
	return redirect(url_for('main.index'))


@bp.post('/process_text')
def process_text():
	try:
		text = request.form.get('raw_text', '').strip()
		if not text:
			return redirect(url_for('main.index'))
		uid = uuid.uuid4().hex
		clauses = segment_clauses(text)
		summary = summarize_text(text)
		risks = analyze_risks(clauses)
		# index for chat
		get_embedding_index().add_document(doc_id=uid, clauses=clauses)
		return render_template('dashboard.html', doc_id=uid, summary=summary, risks=risks, clauses=clauses)
	except Exception as e:
		return f"Error processing text: {str(e)}", 500


