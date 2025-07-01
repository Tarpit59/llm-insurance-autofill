import fitz
import io
import numpy as np
from PIL import Image
from typing import List
from paddleocr import PaddleOCR

ocr_model = PaddleOCR(use_angle_cls=True, lang="en")

class Document_data:
    def __init__(self, metadata, page_content):
        self.metadata = metadata
        self.page_content = page_content

def load_and_ocr_pdf(path: str) -> List[str]:
    pages = []
    doc = fitz.open(path)
    # print('path : ', path)
    for page in doc:
        text = page.get_text()
        # print('text : ', text)
        if len(text.strip()) < 200:
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            np_img = np.array(img)
            results = ocr_model.ocr(np_img)
            # print('results : ', results)
            blocks = []
            if results and results[0]:
                res = results[0]
                for res in list(results):
                    texts = res.get("rec_texts", [])
                    for txt in texts:
                        txt = txt.strip()
                        if txt:
                            blocks.append(txt)
            text = "\n".join(blocks)

        pages.append(text)
    return pages

def load_documents_with_ocr(pdf_dir: str):
    from pathlib import Path
    docs = []
    for pdf in Path(pdf_dir).rglob("*.pdf"):
        pages = load_and_ocr_pdf(str(pdf))
        for i, page in enumerate(pages):
            docs.append(Document_data(page_content=page, metadata={"source": str(pdf), "page": i}))
    print("Documents loaded with OCR.")
    return docs
