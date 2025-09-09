from typing import List, Tuple
import math
import re
from collections import defaultdict


SENTENCE_REGEX = re.compile(r"(?<=[.!?])\s+")


def tokenize_sentences(text: str) -> List[str]:
	text = re.sub(r"\s+", " ", text.strip())
	if not text:
		return []
	sentences = re.split(SENTENCE_REGEX, text)
	return [s.strip() for s in sentences if len(s.strip()) > 0]


def sentence_similarity(a: str, b: str) -> float:
	aw = set(re.findall(r"[a-zA-Z0-9']+", a.lower()))
	bw = set(re.findall(r"[a-zA-Z0-9']+", b.lower()))
	if not aw or not bw:
		return 0.0
	inter = len(aw & bw)
	den = math.log(1 + len(aw)) + math.log(1 + len(bw))
	return inter / max(1e-6, den)


LEGAL_HEADERS = re.compile(r"^(section|clause|article)\s+\d+|^[A-Z][A-Z \-]{3,}$", re.I | re.M)
BOILERPLATE = re.compile(r"(governing law|entire agreement|severability|counterparts|notices|assignment)", re.I)


def _split_by_sections(text: str) -> List[Tuple[str, str]]:
	# Returns list of (header, body)
	lines = text.split('\n')
	sections: List[Tuple[str, str]] = []
	current_header = 'Preamble'
	current_body: List[str] = []
	for ln in lines:
		if LEGAL_HEADERS.search(ln.strip()):
			if current_body:
				sections.append((current_header, '\n'.join(current_body).strip()))
			current_header = ln.strip()
			current_body = []
		else:
			current_body.append(ln)
	if current_body:
		sections.append((current_header, '\n'.join(current_body).strip()))
	return sections


def _filter_boilerplate(sent: str) -> bool:
	return not BOILERPLATE.search(sent)


def textrank_summary(text: str, max_sentences: int = 8) -> str:
	sentences = tokenize_sentences(text)
	if len(sentences) <= max_sentences:
		return ' '.join(sentences)
	# Build similarity graph (sparse)
	n = len(sentences)
	scores = [1.0 for _ in range(n)]
	for _ in range(10):
		new_scores = [0.15 for _ in range(n)]
		for i in range(n):
			for j in range(max(0, i - 20), min(n, i + 20)):
				if i == j:
					continue
				sim = sentence_similarity(sentences[i], sentences[j])
				if sim > 0:
					new_scores[i] += 0.85 * sim * scores[j]
			scores = new_scores
	# Select top sentences by score, keep original order
	idx = list(range(n))
	idx.sort(key=lambda i: scores[i], reverse=True)
	selected = sorted(idx[: max_sentences * 2])
	# Prefer non-boilerplate and cover sections
	sections = _split_by_sections(text)
	selected_sents: List[str] = []
	for i in selected:
		if _filter_boilerplate(sentences[i]):
			selected_sents.append(sentences[i])
		if len(selected_sents) >= max_sentences:
			break
	return ' '.join(selected_sents)


def summarize_text(text: str) -> str:
	length = len(text.split())
	if length < 400:
		k = 6
	elif length < 1500:
		k = 10
	else:
		k = 16
	return textrank_summary(text, max_sentences=k)


