import re
from typing import List


CLAUSE_SPLIT_REGEX = re.compile(r"(?:\n\s*\d+\.\s+)|(?:\n\s*[A-Z][A-Z ]{3,}\n)|(?:\n\s*-{3,}\s*\n)")


def segment_clauses(text: str) -> List[str]:
	if not text:
		return []
	# Normalize spacing
	norm = re.sub(r"\r\n?", "\n", text)
	# Heuristic split by numbered sections, ALL CAPS headings, or divider lines
	parts = CLAUSE_SPLIT_REGEX.split("\n" + norm)
	clauses = [p.strip() for p in parts if p and len(p.strip()) > 30]
	return clauses


