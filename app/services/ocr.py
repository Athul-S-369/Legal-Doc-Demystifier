from pathlib import Path
from typing import List, Optional
import os
import platform
import pytesseract
from PIL import Image
import io
try:
	import pdf2image  # type: ignore
except Exception:
	pdf2image = None
try:
	import PyPDF2  # type: ignore
except Exception:
	PyPDF2 = None


def _configure_tesseract_on_windows() -> None:
	if platform.system().lower() != 'windows':
		return
	custom_cmd = os.environ.get('TESSERACT_CMD')
	if custom_cmd and Path(custom_cmd).exists():
		pytesseract.pytesseract.tesseract_cmd = custom_cmd
		return
	for p in [
		Path(r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"),
		Path(r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"),
	]:
		if p.exists():
			pytesseract.pytesseract.tesseract_cmd = str(p)
			break


_configure_tesseract_on_windows()


def extract_text_from_file(file_path: str) -> str:
	path = Path(file_path)
	collected_text: List[str] = []
	if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}:
		collected_text.append(ocr_image(Image.open(path)))
	elif path.suffix.lower() == '.pdf':
		# Prefer native text if available
		if PyPDF2 is not None:
			try:
				reader = PyPDF2.PdfReader(str(path))
				buf: List[str] = []
				for page in reader.pages:
					try:
						buf.append(page.extract_text() or '')
					except Exception:
						pass
				native_text = '\n'.join(buf).strip()
				if len(native_text) > 50:  # accept shorter too
					return native_text
			except Exception:
				pass
		# OCR fallback using pdf2image if present
		if pdf2image is not None:
			try:
				poppler_path: Optional[str] = os.environ.get('POPPLER_PATH')
				kwargs = {'poppler_path': poppler_path} if poppler_path else {}
				pages = pdf2image.convert_from_path(str(path), dpi=300, **kwargs)
				for page in pages:
					collected_text.append(ocr_image(page))
			except Exception:
				try:
					pages = pdf2image.convert_from_path(str(path), dpi=300)
					for page in pages:
						collected_text.append(ocr_image(page))
				except Exception:
					collected_text.append('')
	else:
		# treat as plain text
		collected_text.append(path.read_text(encoding='utf-8', errors='ignore'))
	return '\n'.join(collected_text)


def ocr_image(image: Image.Image) -> str:
	# Convert to grayscale for better OCR
	gray = image.convert('L')
	return pytesseract.image_to_string(gray)


