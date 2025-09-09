from typing import List, Dict
import re


HIGH_RISK_PATTERNS = [
	(r"indemnif(y|ication|ies)", "Indemnification obligations"),
	(r"liabilit(y|ies).*(unlimited|limitless|no limit)", "Unlimited liability"),
	(r"arbitration|binding arbitration", "Mandatory arbitration"),
	(r"non[- ]?compete|noncompetition", "Non-compete restriction"),
	(r"auto[- ]?renew(al)?", "Auto-renewal clause"),
	(r"unilateral (termination|change|modify)", "Unilateral change/termination"),
	(r"confidentialit(y|ies)", "Broad confidentiality"),
	(r"intellectual property|assign.*invention|work for hire", "IP assignment"),
	(r"liquidated damages", "Liquidated damages"),
	(r"warrant(y|ies) disclaimed|as is", "Warranty disclaimer"),
]

MEDIUM_RISK_PATTERNS = [
	(r"late fee|penalt(y|ies)", "Late fees/penalties"),
	(r"governing law|venue|jurisdiction", "Governing law/venue"),
	(r"force majeure", "Force majeure"),
]


def analyze_risks(clauses: List[str]) -> List[Dict]:
	results: List[Dict] = []
	for idx, clause in enumerate(clauses):
		score = 0
		hits: List[str] = []
		for pat, label in HIGH_RISK_PATTERNS:
			if re.search(pat, clause, flags=re.I):
				score += 3
				hits.append(label)
		for pat, label in MEDIUM_RISK_PATTERNS:
			if re.search(pat, clause, flags=re.I):
				score += 1
				hits.append(label)
		if score > 0:
			results.append({
				'clause_index': idx,
				'score': score,
				'labels': list(sorted(set(hits))),
				'preview': clause[:240]
			})
	# Normalize to 0-100 risk level
	if results:
		max_score = max(r['score'] for r in results)
		for r in results:
			r['risk_percent'] = int(100 * r['score'] / max_score)
	return results


